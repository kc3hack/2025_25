from fastapi import FastAPI, File, UploadFile
import io
import librosa

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # 音声データを読み込む
        audio_data, sr = librosa.load(io.BytesIO(await file.read()), sr=16000)

        # 仮の分類結果
        result = {"osaka": 0.2, "kyoto": 0.5, "hyogo": 0.3, "other": 0.0}

        return result
    except Exception as e:
        return {"error": str(e)}
