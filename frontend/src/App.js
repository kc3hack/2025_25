import { useState } from "react";
import { predictRegion } from "./api"; // API通信を担う関数
import AudioRecorder from './components/AudioRecorder';
import ResultField from './components/ResultField';
import "./App.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>出身地判定アプリ</h1>

        {/* 録音コンポーネント */}
        <AudioRecorder onReceiveResponse={setResult}/>

        {/* 判定結果を出力 */}
        <ResultField result={result}/>
      </header>
    </div>
  );
}

export default App;
