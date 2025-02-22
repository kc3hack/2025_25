from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import librosa
import soundfile as sf
from .analyze_voice import analyze_voice

app = FastAPI()

# CORS設定（フロントエンドのURLを指定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ReactアプリのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     print("aaaa")
#     try:
#         # 音声データを読み込む
#         audio_bytes = await file.read()
#         audio_stream = io.BytesIO(audio_bytes)

#         try:
#             # soundfileで読み込み
#             audio_data, sr = sf.read(audio_stream)
#         except:
#             # soundfileで失敗した場合、librosaを試す
#             audio_stream.seek(0)
#             audio_data, sr = librosa.load(audio_stream, sr=None)

#         # 仮の分類結果（AIモデルに置き換える予定）
#         result = {"osaka": 0.2, "kyoto": 0.5, "hyogo": 0.3, "other": 0.0}

#         return {"success": True, "result": result}
#     except Exception as e:
#         return {"success": False, "error": str(e)}

# 音声データを受け取り、AI判定を行うエンドポイント
@app.post("/upload")
async def upload_audio(request: Request):
    try:
        # 音声データを受け取る
        audio_data = await request.body()
        print(f"受け取った音声データの長さ: {len(audio_data)} バイト")
        audio_stream = io.BytesIO(audio_data)
        
        ##audio_data, sr = sf.read(audio_stream)
        audio_stream.seek(0)
        with open("./test.wav", 'wb') as f:
            f.write(audio_data)
        audio_data, sr = librosa.load(audio_stream, sr=None)
        

        

        # AIモデルで判定（仮の処理）
        result = analyze_voice(audio_data,sr) # 仮の結果を返す

        # 結果を返す
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 簡単な動作確認用のルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "API is running!"}
