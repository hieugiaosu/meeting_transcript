# Meeting Transcription Project

## Idea

This project provides an automated solution for transcribing meetings. The system detects human speech, transcribes it, and identifies the speaker.

## Technical Components

### Voice Activity Detection (VAD)

We use a VAD module to detect human speech activity. The VAD module used in this project can be found at [ricky0123/vad](https://github.com/ricky0123/vad?tab=readme-ov-file).

### Automatic Speech Recognition (ASR)

For transcription, we use the Whisper ASR model, specifically the small English version. More information about Whisper can be found [here](https://huggingface.co/openai/whisper-small.en).

### Speaker Embedding

We have developed a custom model to identify the speaker. The model structure includes:

- **Preprocessing**: Resampling audio to 16 kHz.
- **Mel Spectrogram**: Parameters include `nfft=256`, `n_mel=64`, `hoplength=160`.
- **Model Architecture**: Linear layer -> Positional encoding -> 3 Transformer encoder layers -> Linear layer.
- **Output**: 256-dimensional vector.

#### Training

- **Dataset**: The model is trained on the [LibriSpeech 100-hour clean dataset](https://www.openslr.org/12).
- **Loss Function**: We use ArcFace loss, which is described in the paper [Additive Angular Margin Loss for Deep Face Recognition](https://arxiv.org/abs/1801.07698).

## Workflow

1. **Speaker Speech**: The system captures the speaker's speech.
2. **VAD Detection**: The VAD module detects speech activity.
3. **ASR Transcription**: Detected speech is sent to the ASR model for transcription.
4. **Speaker Identification**: Transcribed speech is sent to the speaker embedding model to determine the speaker.

## Technology Stack

### Frontend

- **ReactJS**: For building the user interface.

### Backend

- **FastAPI**: For building the backend API, structured in MVC style.

### Messaging and Caching

- **RabbitMQ**: For message queuing.
- **Redis**: For caching the results.

### Consumer

- **Consumer Service**: Processes the audio by applying model inference.

## Application Workflow

1. The user initiates the process through the web UI by pressing "Start".
2. The frontend requests a connection ID from the backend. This ID is used to access results later and is stored in both the frontend and Redis.
3. Each time VAD detects speech, the audio is sent to the backend. The server puts the speech into RabbitMQ.
4. The consumer processes the speech to transcribe it and identify the speaker. Results are put back into Redis.
5. Every 2 seconds, the web UI requests the server to retrieve the latest results from Redis.

## Running Locally

### Prerequisites

- Docker
- Node.js and npm

### Backend

To run the backend locally, use the following commands:

```sh
docker-compose up --build
```

### Frontend

To run the frontend locally, navigate to the frontend directory and use the following command:

```sh
npm run dev
```

## Additional Setup

- Ensure that RabbitMQ and Redis services are running and properly configured.
- Update environment variables as necessary for your local setup.

## References

- [Voice Activity Detection Module](https://github.com/ricky0123/vad?tab=readme-ov-file)
- [Whisper ASR Model (available on Huggingface)](https://huggingface.co/openai/whisper-small.en)
- [LibriSpeech Dataset](https://www.openslr.org/12)
- [ArcFace Loss](https://arxiv.org/abs/1801.07698)

## Additional Information

- Follow best practices for handling asynchronous tasks and error management.
- Regularly update the models and dependencies to leverage improvements and new features.
- This project aims to streamline meeting transcription by combining advanced speech recognition and speaker identification technologies, ensuring accurate and efficient transcriptions.
