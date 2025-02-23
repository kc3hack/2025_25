import torchaudio
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from .analyze_voice import analyze_voice

app = FastAPI()

# CORS設定（フロントエンドのURLを指定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],  # ReactアプリのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 音声データを受け取り、AI判定を行うエンドポイント
@app.post("/upload")
async def upload_audio(request: Request):
    try:
        # 音声データを受け取る
        audio_data = await request.body()
        print(f"受け取った音声データの長さ: {len(audio_data)} バイト")
        audio_stream = io.BytesIO(audio_data)
        
       
        audio_data, sr =torchaudio.load(audio_stream)
        audio_data=audio_data.detach().cpu().numpy()
        if audio_data.shape[1]/sr<5:
            result={"name": "error", "content": "音声の長さが短すぎます"}
        else:
            result = analyze_voice(audio_data,sr) 
       
        # 結果を返す
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 簡単な動作確認用のルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "API is running!"}
