from fastapi import FastAPI, File, UploadFile
import io
import librosa
import soundfile as sf  # soundfileを追加

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # 音声データを読み込む（soundfile経由で安定化）
        audio_bytes = await file.read()
        audio_data, sr = sf.read(io.BytesIO(audio_bytes))

        # 仮の分類結果（ここを後でAIモデルの結果に置き換える予定）
        result = {"osaka": 0.2, "kyoto": 0.5, "hyogo": 0.3, "other": 0.0}

        return result
    except Exception as e:
        return {"error": str(e)}

# 簡単な動作確認用のルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "API is running!"}
