import { useState, useEffect } from "react";
import "./ResultField.css"; // スタイルファイルを追加

const ResultField = (props) => {
  const [visible, setVisible] = useState(false);
  const result = props.result;

  useEffect(() => {
    if (result) {
      setVisible(true); // 新しい結果を受け取ったら表示
    }
  }, [result]);

  const handleClose = () => {
    setVisible(false);
  };

  return (
    <div className={`result-container ${visible && result ? "show" : ""}`}>
      {visible && result && (
        <div className="result-box">
          <h2>判定結果😎</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
          <button onClick={handleClose} className="close-button">閉じる</button>
        </div>
      )}
    </div>
  );
};

export default ResultField;
