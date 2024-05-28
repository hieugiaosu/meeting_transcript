import torch
import torchaudio
from torch.utils.data import Dataset
from model import processor

class SpeakerEmbeddingDataset(Dataset):
    def __init__(self,data,sample_rate=16000,window_length=0.1,max_chunk_num = 50):
        super().__init__()
        self.data = data
        self.sample_rate = sample_rate
        self.window_length = int(window_length*sample_rate)
        self.max_chunk_num = max_chunk_num
        self.max_audio_length = 16000*5
        self.proc = processor()
        
    def __len__(self): return len(self.data)*2
    def __getitem__(self,idx):
        i = idx//2
        r = idx%2
        row = self.data.iloc[i]
        audio,rate = torchaudio.load(row['audio_file'])
        audio = audio.squeeze()
        if r==0:
            audio = audio[:audio.shape[0]//2]
        else:
            audio = audio[audio.shape[0]//2:]
        if audio.shape[0] < self.max_audio_length:
            padding_size = self.max_audio_length - audio.shape[0]
            padding = torch.zeros(padding_size).float()
            audio = torch.cat([padding,audio],dim = 0)
        elif audio.shape[0]> self.max_audio_length:
            audio = audio[:self.max_audio_length]
        audio = self.proc(audio)
        speaker = torch.tensor([int(row['speaker'])])
        return audio,speaker