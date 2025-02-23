import { useState } from "react";
import Logo from './components/Logo';
import ReadingScript from "./components/ReadingScript";
import AudioRecorder from './components/AudioRecorder';
import ResultField from './components/ResultField';
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [recording, setRecording] = useState(false);

  return (
    <div className="App">
      <header className="App-header">
        <Logo />

        <h1>出身地判定アプリ</h1>
        
        <ReadingScript recording={recording} />
        <br />
        
        {/* 録音コンポーネント */}
        <AudioRecorder onReceiveResponse={setResult} setRecording={setRecording} />
        <br />

        {/* 判定結果を出力 */}
        <ResultField result={result} />
      </header>
    </div>
  );
}

export default App;
