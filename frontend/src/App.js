import { useState } from "react";
import { predictRegion } from "./api"; // API通信を担う関数
import AudioRecorder from './components/AudioRecorder';
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null); // 録音データを保存

  // 録音データが取得されたときに呼び出される
  const handleAudioData = (blob) => {
    setAudioBlob(blob);
  };

  const handlePredict = async () => {
    if (!audioBlob) {
      alert("音声を録音してください");
      return;
    }

    try {
      const prediction = await predictRegion(audioBlob);
      setResult(prediction);
    } catch (error) {
      console.error("Error during prediction:", error);
      setResult({ error: "エラーが発生しました" });
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>出身地判定アプリ</h1>

        {/* 録音コンポーネント */}
        <AudioRecorder onAudioData={handleAudioData} />

        <button onClick={handlePredict} disabled={!audioBlob}>
          音声を送信
        </button>

        {result && (
          <div>
            <h2>判定結果</h2>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
