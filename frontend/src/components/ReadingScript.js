import { useEffect, useState } from "react";

const scripts = [
    "こんにちは！", "天気がいいですね", "今日は何をしますか？", "好きな食べ物は何ですか？",
    "旅行に行きたい場所は？", "最近読んだ本は？", "趣味は何ですか？", "週末の予定は？"
];
  
const ReadingScript = () => {
    const [displayScripts, setDisplayScripts] = useState([]);

    useEffect(() => {
        // 3つのランダムなスクリプトを選ぶ
        const shuffled = [...scripts].sort(() => 0.5 - Math.random()).slice(0, 3);
        setDisplayScripts(shuffled);
    }, []);
    
    return (<>
        <p>読んでみてください：</p>
        {/* ランダムなスクリプトを図形の中に表示 */}
        <div className="script-container">
            {displayScripts.map((script, index) => (
                <div key={index} className="script-box">{script}</div>
            ))}
        </div>
    </>)
};

export default ReadingScript;