from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# ダミーAIモデルの例
def dummy_predict_region(audio_data):
    # 音声データをAIモデルで処理（ダミーの結果を返す）
    return {"region": "大阪", "probability": 0.95}

@app.post("/upload")
async def upload_audio(request: Request):
    try:
        # 音声データを受け取る
        audio_data = await request.body()
        print(f"受け取った音声データの長さ: {len(audio_data)} バイト")

        # AIモデルで判定（仮の処理）
        result = dummy_predict_region(audio_data)

        # 結果を返す
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
