import { useState, useEffect, useContext } from "react";
import { useMicVAD } from "@ricky0123/vad-react";
import axios from "axios";
import { apiBaseURL } from '../utils/globalConfig';
import { TranscriptContext } from "../context/TranscriptContext";

const VAD = () => {
    const { addTranscript,setAlReadyRead,alreadyRead } = useContext(TranscriptContext);
    const [connectionString, setConnectionString] = useState("");
    const [stop, setStop] = useState(false);
    const [count, setCount] = useState(0);
    const [finalCount,setFinalCount] = useState(0)

    const vad = useMicVAD({
        onSpeechEnd: async (audio) => {
            setCount(count + 1);
            const audio_arr = []
            for (var i in audio){
                audio_arr.push(audio[i])
            }
            await handleSpeechEnd(audio_arr);
        },
    });

    useEffect(() => {
        const getConnectionString = async () => {
            if (!connectionString) {
                const res = await axios.get(`${apiBaseURL}`);
                setConnectionString(res.data.secret_id);
            }
        };
        getConnectionString();
    }, [connectionString]);

    const fetchTranscript = async (isFinal = false) => {
        if (isFinal && alreadyRead >= finalCount) return
        console.log('------')
        let config = {
            headers: {
                "Content-Type": "application/json",
            },
        };
        const transcriptRes = await axios.put(
            `${apiBaseURL}speech/${connectionString}`,
            {
                from_number: alreadyRead + 1,
                to_number: count,
            },
            config
        );
        setAlReadyRead(parseInt(transcriptRes.data.to_number));
        for (let i in transcriptRes.data.transcript) {
            let content = `${parseInt(transcriptRes.data.from_number)+parseInt(i)+1}: speaker ${transcriptRes.data.speakers[i]}: ${transcriptRes.data.transcript[i]}`;
            if (content) addTranscript(content);
        }
    };

    const handleSpeechEnd = async (audio) => {
        
        const arrayBlob = new Blob([JSON.stringify(audio)], {
            type: "application/json",
        });
        const arrayFile = new File([arrayBlob], "arrayData.json");

        let config = {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        };
        const formData = new FormData();
        formData.append("audio", arrayFile);
        formData.append("sample_rate", 16000);
        formData.append("request_number", count);
        formData.append("end_request", stop);
        await axios.post(`${apiBaseURL}speech/${connectionString}`, formData, config);
        
    };

    const handleStopRecording = async () => {
        await vad.pause();
        // delete vad;
        if (!stop) {
            setTimeout(() => {
                setStop(true);
                setFinalCount(count-1)
            }, 800);
            
        }
    };

    useEffect(() => {
        const intervalId = setInterval(() => fetchTranscript(stop), 2000);
        return () => clearInterval(intervalId);
    }, [connectionString, vad.listening, alreadyRead, count]);

    return !stop?(
        <>
            {vad.userSpeaking ? (
                <img
                    src="src/assets/image_processing20210908-6634-tk570d.gif"
                    width="70%"
                    className="onSpeech"
                    alt="On Speech"
                />
            ) : (
                <div className="circle"></div>
            )}
            <button
                type="button"
                className="btn btn-danger rounded-pill btn-lg stop-transcript mt-0"
                onClick={handleStopRecording}
            >
                Stop Now
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    fill="currentColor"
                    className="bi bi-stop-fill"
                    viewBox="0 0 16 16"
                >
                    <path d="M5 3.5h6A1.5 1.5 0 0 1 12.5 5v6a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 11V5A1.5 1.5 0 0 1 5 3.5" />
                </svg>
            </button>
        </>
    ):(<>
        <div>
            <h1 className="text-primary">{alreadyRead<finalCount?"Đợi xử lý":"Hoàn tất"}</h1>
        </div>
    </>);
};

export default VAD;
