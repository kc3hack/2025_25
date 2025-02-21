import { useState } from "react";
import { predictRegion } from "./api";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    // 仮の音声データ（録音機能がないため）
    const audioBlob = new Blob(["dummy audio data"], { type: "audio/wav" });

    const prediction = await predictRegion(audioBlob);
    setResult(prediction);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>出身地判定アプリ</h1>
        <button onClick={handlePredict}>音声を送信</button>

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
