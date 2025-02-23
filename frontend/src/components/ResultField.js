import { useEffect, useState } from "react";
import "./ResultField.css"; // スタイルファイルを追加


const ResultField = (props) => {
  const [show, setShow] = useState(false);
  const result = props.result;

  useEffect(() => {
    if (result) {
      setShow(true);
    }
  }, [result]);

  return (
    <div className={`result-container ${show ? "show" : ""}`}>
      {result && (
        <div className="result-box">
          <h2>判定結果 🎤</h2>

          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ResultField;
