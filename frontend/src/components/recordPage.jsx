import React, { useContext, useEffect, useState } from 'react';
import Example from './example';
import VAD from './VAD';
import { TranscriptContext } from '../context/TranscriptContext';

const RecordScreen = () => {
    const [isRecord, setRecord] = useState(false);
    const { transcript } = useContext(TranscriptContext);

    const renderTranscript = () => {
        return [...transcript].map((entry, index) => (
            <React.Fragment key={index}>
                <strong className={index % 2 === 0 ? 'text-danger' : 'text-success'}>
                    {entry}
                </strong><br></br>
            </React.Fragment>
        ));
    };

    const downloadTranscript = () => {
        const transcriptArray = Array.from(transcript);
        const element = document.createElement('a');
        const file = new Blob([transcriptArray.join('\n')], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = 'transcript.txt';
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
        document.body.removeChild(element);
    };

    return (
        <div className="record-screen row vh-100">
            <div className="col-md-9 record m-0 p-0">
                {isRecord ? (
                    <VAD />
                ) : (
                    <button
                        type="button"
                        className="btn btn-primary rounded-pill btn-lg start-transcript mt-0"
                        onClick={() => {
                            setRecord(true);
                        }}
                    >
                        Start Now
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="18"
                            height="18"
                            fill="currentColor"
                            className="bi bi-mic-fill"
                            viewBox="0 0 16 16"
                        >
                            <path d="M5 3a3 3 0 0 1 6 0v5a3 3 0 0 1-6 0z" />
                            <path d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5" />
                        </svg>
                    </button>
                )}
            </div>
            <div className="col-md-3">
                <div className="row text-center p-0 justify-content-center">
                    <h2>Your Transcript Here</h2>
                    <button className="btn btn-primary btn-small w-auto" onClick={downloadTranscript}>
                        Download Transcript
                    </button>
                </div>
                <div className="transcription row vh-100 pb-2" style={{ maxHeight: '100vh', overflowY: 'auto' }}>
                    {!isRecord ? <Example /> : null}
                    <div>{renderTranscript()}</div>
                </div>
            </div>
        </div>
    );
};

export default RecordScreen;
