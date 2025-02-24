import { useEffect, useState } from "react";
import Logo from "./components/Logo";
import ReadingScript from "./components/ReadingScript";
import AudioRecorder from './components/AudioRecorder';
import ResultField from './components/ResultField';
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [recording, setRecording] = useState(false);
  const [waiting, setWaiting] = useState(false);

  useEffect(() => {
    setResult(null);
  }, [result]);

  return (
    <div className="App">
      <header className="App-header">
        <Logo />

        <h1>出身地判定 AI</h1>
        
        {recording && (<>
          <ReadingScript />
          <br />
        </>)}
        
        {/* 録音コンポーネント */}
        <AudioRecorder onReceiveResponse={setResult} setRecording={setRecording} setWaiting={setWaiting} />
        <br />

        {/* 判定結果を出力 */}
        <ResultField result={result} recording={recording} waiting={waiting} />
      </header>
    </div>
  );
}

export default App;
