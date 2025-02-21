export async function predictRegion(audioBlob) {
    const formData = new FormData();
    formData.append("file", audioBlob, "audio.wav"); // "file" は FastAPI のエンドポイントで受け取るキーと合わせる

    try {
        const response = await fetch("http://localhost:8000/predict", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("API request failed");
        }

        return await response.json(); // JSONデータを返す
    } catch (error) {
        console.error("Error:", error);
        return null;
    }
}
