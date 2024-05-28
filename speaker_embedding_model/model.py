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

class ArcFace(nn.Module):
    """
This is my reimplement of the ArcFace loss function
    """
    def __init__(self,numClasses,embeddingSize,margin,scale,eps=1e-6):
        super().__init__()
        self.numClasses = numClasses
        self.embeddingSize = embeddingSize
        self.m = margin
        self.s = scale
        self.eps = eps
        self.W = nn.Parameter(torch.Tensor(numClasses, embeddingSize))
        nn.init.xavier_normal_(self.W)
    def forward(self,embeddings,labels=None):
        if labels is not None:
            batch_size = labels.size(0)
            cos = F.linear(F.normalize(embeddings), F.normalize(self.W))
            one_hot_encoding_labels = torch.zeros(batch_size, self.numClasses, device=labels.device)
            one_hot_encoding_labels.scatter_(1, labels.unsqueeze(-1), 1)
            cos_target_classes = cos[one_hot_encoding_labels==1]
            theta =  torch.acos(torch.clamp(cos_target_classes, -1 + self.eps, 1 - self.eps))
            cos_with_margin = torch.cos(theta+self.m)
            diff = (cos_with_margin-cos_target_classes).unsqueeze(1)
            logits = cos + one_hot_encoding_labels*diff
            logits = self.s*logits
            return logits
        else:
            cos = F.linear(F.normalize(embeddings), F.normalize(self.W))
            return cos
        
class ModelWithArcFaceForTraining(nn.Module):
    def __init__(self):
        super().__init__()
        self.emb = SpeakerEmbedding(64,128,256)
        self.arcFace = ArcFace(256,256,0.4,64)
    def forward(self,x,labels=None):
        y = self.emb(x)
        logits = self.arcFace(y,labels)
        return logits