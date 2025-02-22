from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],  # すべてのオリジンを許可（開発時のみ）
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

def dummy_predict_region(audio_data):
    return {"region": "大阪", "probability": 0.95}

@app.post("/upload")
async def upload_audio(request: Request):
    try:
        # 🔹 音声データを受け取る
        audio_data = await request.body()
        print(f"受け取った音声データの長さ: {len(audio_data)} バイト")

        # 🎯 AIモデルで判定（仮の処理）
        result = dummy_predict_region(audio_data)

        # ✅ 結果を返す
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}
