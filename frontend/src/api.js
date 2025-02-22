export const predictRegion = async (audioBlob) => {
  try {
      const formData = new FormData();
      formData.append("file", audioBlob, "audio.wav");

      const response = await fetch("http://127.0.0.1:5000/predict", {
          method: "POST",
          body: formData,
      });

      if (!response.ok) {
          throw new Error("サーバーからエラーが返されました");
      }

      const result = await response.json();
      return result;
  } catch (error) {
      console.error("APIエラー:", error);
      throw error; // エラーを再スローしてApp.jsで処理
  }
};
