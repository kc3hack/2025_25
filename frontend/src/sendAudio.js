async function sendAudio(blob) {
    const formData = new FormData();
    formData.append("file", blob, "audio.wav");

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();
    console.log("Prediction result:", data);
}

export default sendAudio;
