import { useState, useEffect } from "react";
import AudioRecorder from './components/AudioRecorder';
import ResultField from './components/ResultField';
import "./App.css";

const scripts = [
  "こんにちは！", "天気がいいですね", "今日は何をしますか？", "好きな食べ物は何ですか？",
  "旅行に行きたい場所は？", "最近読んだ本は？", "趣味は何ですか？", "週末の予定は？"
];

function App() {
  const [result, setResult] = useState(null);
  const [displayScripts, setDisplayScripts] = useState([]);

  useEffect(() => {
    // 3つのランダムなスクリプトを選ぶ
    const shuffled = [...scripts].sort(() => 0.5 - Math.random()).slice(0, 3);
    setDisplayScripts(shuffled);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>出身地判定アプリ</h1>
        
        <p>読んでみてください：</p>
        {/* ランダムなスクリプトを図形の中に表示 */}
        <div className="script-container">
          {displayScripts.map((script, index) => (
            <div key={index} className="script-box">{script}</div>
          ))}
        </div>
        
        {/* 録音コンポーネント */}
        <AudioRecorder onReceiveResponse={setResult} />

        {/* 判定結果を出力 */}
        <ResultField result={result} />
      </header>
    </div>
  );
}

export default App;
