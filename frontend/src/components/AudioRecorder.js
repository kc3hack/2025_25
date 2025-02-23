import { useState } from "react";
import "./AudioRecorder.css";

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

    return result;
  } catch (error) {
    console.error("音声データ送信エラー:", error);
    return {"type": "error", "contents": "音声データの送信に失敗しました..."};
  }
};

const createRecording = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream);

  recorder.start()

  const getAudioBrob = async () => {
    const promise = new Promise((res, rej)=>{
      recorder.ondataavailable = (event) => {
        res(new Blob([event.data], { type: "audio/wav" }))
      }
    })

    recorder.stop()

    return promise
  }

  return {get: ()=>getAudioBrob()};
};

const endRecording = async (recording) => {
  if(recording === null) throw new Error();

  const audioBlob = await recording.get();

  const arrayBuffer = await audioBlob.arrayBuffer();
  const result = await sendAudio(arrayBuffer);

  return result;
};

const AudioRecorder = (props) => {
  const [recording, setRecording] = useState(null);

  const onButtonClick = async ()=>{
    if(recording === null){
      setRecording(await createRecording());
    }
    else{
      setRecording(null);
      props.onReceiveResponse(await endRecording(recording));
    }
  }

  return (
    <button className="recording-button" data-recording={recording !== null} onClick={onButtonClick}>
      {recording === null ? "録音開始" : "送信"}
    </button>
  );
};

export default AudioRecorder;
