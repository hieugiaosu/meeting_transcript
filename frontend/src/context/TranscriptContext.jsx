import React, { createContext, useState } from 'react';

// Create the context
export const TranscriptContext = createContext();

// Create a provider component
export const TranscriptProvider = ({ children }) => {
    const [transcript, setTranscript] = useState(new Set());
    const [alreadyRead, setAlReadyRead] = useState(-1);
    const addTranscript = (newEntry) => {
        setTranscript(prev => new Set(prev).add(newEntry));
    };

    return (
        <TranscriptContext.Provider value={{ transcript, addTranscript,alreadyRead,setAlReadyRead }}>
            {children}
        </TranscriptContext.Provider>
    );
};
