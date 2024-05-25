import torch
import torchaudio
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

class WhisperInference:
    def __init__(self,device = 'cpu'):
        self.processor = AutoProcessor.from_pretrained("openai/whisper-small.en")
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-small.en")
        self.model.to(device)
        self.model.eval()
    def __call__(self,audio,sample_rate):
        audio = torch.tensor(audio)
        torchaudio.save("test.wav", audio.unsqueeze(0), sample_rate)
        if sample_rate != 16000:
            audio = torchaudio.functional.resample(audio,sample_rate,16000)
        audio = audio.squeeze()
        with torch.no_grad():
            inputs = self.processor(
                audio,
                sampling_rate=16000, 
                return_tensors="pt"
                )
            input_features = inputs.input_features
            generated_ids = self.model.generate(inputs=input_features)
            transcription = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return transcription