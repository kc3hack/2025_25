import { useState, useEffect } from "react";
import "./ResultField.css"; // スタイルファイルを追加

const ScceedResult = (probs) => {
  const content = probs.content;

  let max = {key: null, value: 0};
  const percentages = {};
  for(const key in content){
    const percentage = content[key] * 100
    percentages[key] = (percentage < 10 ? " " : "") + String(Math.floor(percentage));

    if(max.value < percentage) max = {key: key, value: percentage}
  }

  return <>
    <pre>
      大阪 : {percentages["大阪"]} % {"\n"}
      京都 : {percentages["京都"]} % {"\n"}
      兵庫 : {percentages["兵庫"]} % {"\n"}
    </pre>
    <pre>あなたは {max.key}人 です！</pre>
  </>
}

const FailedResult = () => <pre>分析に失敗しました。再度、５秒以上話してから送信してください。</pre>

const ResultAnalysis = (probs) => {
  const result = probs.result;

  const faces = "😎 😋 😃 😇 😂 🤪 🤗 🤖".split(" ")
  const face = faces[Math.floor(Math.random() * faces.length)]

  return (<>
    <h2>判定結果{face}</h2>
    {
      result.type === "success" ?
      <ScceedResult content={result.content} /> :
      <FailedResult />
    }
  </>)
}

const WaitingField = () => {
  return (<>
    <pre>分析中です、少々お待ちください...</pre>
  </>)
}

const ResultField = (props) => {
  const [current, setCurrent] = useState(null);

  const result = props.result;
  const recording = props.recording;
  const waiting = props.waiting;

  useEffect(() => {
    if (result) setCurrent(result); // 新しい結果を受け取ったら表示
    if (recording) setCurrent(null);
  }, [result, recording]);

  console.log(waiting)

  return (
    <div className={`result-container show`}>
      {
        waiting ?
        <WaitingField /> :
        <>
          {current !== null &&
            <div className="result-box">
              {
                <ResultAnalysis result={current}/>
              }
              <button onClick={() => setCurrent(null)} className="close-button">閉じる</button>
            </div>
          }
        </>
      }
    </div>
  );
};

export default ResultField;
