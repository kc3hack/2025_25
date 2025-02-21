export const predictRegion = async (audioBlob) => {
    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/octet-stream", // バイナリデータを送信
        },
        body: audioBlob, // ダミーデータを送信
      });
  
      if (!response.ok) {
        throw new Error("ネットワークエラーが発生しました");
      }
  
      const result = await response.json();
      return result;
    } catch (error) {
      console.error("APIエラー:", error);
      throw error; // エラーを再スローしてApp.jsで処理
    }
  };
  