import { useEffect, useState } from "react";

const scripts = [
    "朝の電車が空いていてラッキーだと思ったのに、座った瞬間に椅子が濡れていることに気づいて、本当に最悪だった",
"コンビニで買い物をしてレジに並んだとき、財布を忘れたことに気づいて、すごく恥ずかしかった。",
"天気予報では晴れるって言ってたのに、家を出た瞬間に雨が降ってきて、傘を持っていなくて困った。",
"ラーメン屋さんで『にんにく入れますか？』って聞かれると、毎回悩むけど結局入れちゃうんだよね。",
"寝る前にスマホをやめようと思っているのに、気づいたら朝までずっと動画を見てしまっていることがよくある。",
"エレベーターに乗ろうと走って行ったら、閉まりかけのドア越しに中の人と目が合って、なんだか気まずかった。", 
"昨日の試合見た？最後の逆転、本当に熱かったよね。思わず声が出ちゃったよ。", 
"知らない番号から電話がかかってきて、出たら『間違えました』って言われて、ちょっとびっくりした。",
"お好み焼きと白ご飯の組み合わせって、やっぱり最強だと思うんだけど、みんなはどう思う？", 
"洗濯物を干した途端に空が曇ってきて、これは絶対に雨が降るやつだと思いながら急いで取り込んだ。"
];
  
const ReadingScript = () => {
    const [displayScripts, setDisplayScripts] = useState([]);

    useEffect(() => {
        // 3つのランダムなスクリプトを選ぶ
        const shuffled = [...scripts].sort(() => 0.5 - Math.random()).slice(0, 1);
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