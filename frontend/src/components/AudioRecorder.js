import { useState, useRef } from "react";

const AudioRecorder = (props) => {
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.current = new MediaRecorder(stream);

    mediaRecorder.current.ondataavailable = (event) => {
      
      audioChunks.current.push(event.data);
    };

    mediaRecorder.current.onstop = async () => {
      
      const audioBlob = new Blob(audioChunks.current, { type: "audio/wav" });
      
      // バイナリ化
      const arrayBuffer = await audioBlob.arrayBuffer();
     
      // バックエンドに送信
      await sendAudio(arrayBuffer);


      // 録音データをリセット
      audioChunks.current = [];
    };

    mediaRecorder.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorder.current && recording) {
      mediaRecorder.current.stop();
      setRecording(false);
    }
    audioChunks.current = []; // 録音データをリセット
  };

  const sendAudio = async (audioData) => {
    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/octet-stream",
        },
        body: audioData,
      });

      const result = await response.json();
      console.log("サーバーからのレスポンス:", result);

      props.onReceiveResponse(result)
    } catch (error) {
      console.error("音声データ送信エラー:", error);
    }
  };

  return (
    <div>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "停止" : "録音開始"}
      </button>
    </div>
  );
};

export default AudioRecorder;
