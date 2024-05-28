import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

def processor(sample_rate=16000,n_fft=400,hop_length=160,f_min=80,f_max=4000,n_mels=64):
    f = torchaudio.transforms.MelSpectrogram(sample_rate=sample_rate,
                                             n_fft=n_fft,hop_length=hop_length,
                                             f_min=f_min,f_max=f_max,
                                             n_mels=n_mels)
    def proc(audio):
        with torch.no_grad():
            mel = f(audio)
            mel = torch.log(1+mel)
            mel = torch.tanh(mel)
        return mel
    return proc

class SpeakerEmbedding(nn.Module):
    def __init__(self,input_dim,hidden_state_dim,embedding_dim):
        super().__init__()
        self.input_transform = nn.Sequential(
            nn.Linear(input_dim,hidden_state_dim),
            nn.ELU(),
            nn.Linear(hidden_state_dim,hidden_state_dim),
            nn.ELU()
        )
        
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=2*hidden_state_dim, nhead=2, activation='relu',batch_first=True),
            num_layers = 2
        )
        
        self.fc = nn.Linear(2*hidden_state_dim,embedding_dim)
       
        self.hidden_state_dim = hidden_state_dim
        self.embedding_dim = embedding_dim
        self.input_dim = input_dim
    def forward(self,x):
        batch_size = x.shape[0]
        seq_len = x.shape[2]
        i = torch.transpose(x,1,2)
        i = self.input_transform(i)
        pos = self.get_sinusoidal_positional_encoding(seq_len,self.hidden_state_dim,i.device).expand(batch_size,-1,-1)
        q = torch.cat([i,pos],dim = -1)
        att = self.transformer(q)
        o = self.fc(att[:,-1,:])
        return o
    def get_sinusoidal_positional_encoding(self, max_len, d_model,device=None):
        position = torch.arange(max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * -(np.log(10000.0) / d_model))

        pos_encoding = torch.zeros((max_len, d_model))
        pos_encoding[:, 0::2] = torch.sin(position * div_term)
        pos_encoding[:, 1::2] = torch.cos(position * div_term)
        pos_encoding = pos_encoding.to(device)
        return pos_encoding
    
class SpeakerEmbeddingInference:
    def __init__(self,path=""):
        self.processor = processor()
        self.model = SpeakerEmbedding(64,128,256)
        self.device = 'cpu'
        if path != "":
            self.model.load_state_dict(torch.load(path,map_location=self.device))
        self.model.eval()
        
    def __call__(self,audio,sample_rate=16000):
        if isinstance(audio,list):
            x = torch.tensor(audio,device=self.device).float()
        if sample_rate != 16000:
            x = torchaudio.functional.resample(x,sample_rate,16000)
        if x.dim() == 1:
            x = x.unsqueeze(0)
        with torch.no_grad():
            mel = self.processor(x)
            e = self.model(mel)
            e = F.normalize(e)
        return e
