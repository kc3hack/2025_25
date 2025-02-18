from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import LlamaTokenizerFast, LlamaForCausalLM

import torch
import os
import math

def generate(tokenizer: LlamaTokenizerFast, model: LlamaForCausalLM, prompt: str) -> str:
    device = model.device

    tokenized = tokenizer(prompt, return_tensors="pt")
    input_ids = tokenized.input_ids.to(device=device)
    attention_mask = tokenized.attention_mask.to(device=device)

    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_new_tokens=1024,
        pad_token_id=tokenizer.eos_token_id,
    )

    decoded = tokenizer.batch_decode(output, skip_special_tokens=True)[0]

    return decoded

def summary_channel_transcripts(tokenizer: LlamaTokenizerFast, model: LlamaForCausalLM, dir_path: str) -> None:
    paths = os.listdir(dir_path)

    transcribe = ""
    for path in paths:
        with open(dir_path + path, mode="r") as f:
            transcribe += f.read() + "\n\n"

    cap = 5000
    for i in range(math.ceil(len(transcribe) / cap)):
        segment = transcribe[i*cap : (i+1)*cap]

        prompt = "<｜User｜>\n\n以下は、ある日本のYouTubeチャンネルの動画音声を文字起こししたものです。\n文章の内容から、以下の情報を見つけ出し、返しなさい\n\n- チャンネル名（または話し手の名前）\n- チャンネルのジャンル\n- 話し手の出身地（日本の都道府県単位）\n- 話し口調から推定される方言の地方\n\nわからない項目は不明で構いません。\n最終的な回答は<answer></answer>の中に一行づつ改行して答えなさい。\n\n以下、動画の文字起こしです。\n\n\n---\n\n"

        prompt += segment
        prompt += "\n\n---\n\n\n<｜Assistent｜>\n<think>\n"

        decoded = generate(tokenizer, model, prompt)

        with open(dir_path + "0" * (4 - len(str(i))) + str(i) + ".txt", mode="w") as f:
            f.write(decoded)

def main():
    model_id = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
    tokenizer = AutoTokenizer.from_pretrained(model_id); assert isinstance(tokenizer, LlamaTokenizerFast)
    model = AutoModelForCausalLM.from_pretrained(model_id); assert isinstance(model, LlamaForCausalLM)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model.to(device=device) #type: ignore

    dir_path = "./src/assets/text/JTubeSpeech/"
    channel_ids = os.listdir(dir_path)

    for channel_id in channel_ids:
        summary_channel_transcripts(tokenizer, model, dir_path + channel_id + "/")

if __name__ == "__main__":
    main()