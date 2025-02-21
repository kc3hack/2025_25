import whisper
import os
import math
import torch

from functools import reduce

from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import LlamaTokenizerFast, LlamaForCausalLM

class AudioSummarizer:
    def __init__(self):
        self.whisper = whisper.load_model("small")

        model_id = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
        llama_tokenizer = AutoTokenizer.from_pretrained(model_id)
        llama = AutoModelForCausalLM.from_pretrained(model_id)

        assert isinstance(llama_tokenizer, LlamaTokenizerFast)
        assert isinstance(llama, LlamaForCausalLM)

        llama.to(device="cuda" if torch.cuda.is_available() else "cpu") #type: ignore

        self.llama_tokenizer = llama_tokenizer
        self.llama = llama

    def _transcribe(self, file_path: str) -> str:
        assert os.path.isfile(file_path)

        result = self.whisper.transcribe(file_path)["text"]
        assert type(result) is str

        return result

    def _summarize_text(self, text: str) -> list[str]:
        summaries = []

        cap = 5000
        for i in range(math.ceil(len(text) / cap)):
            segment = text[i*cap : (i+1)*cap]

            prompt = "<｜User｜>\n\n以下は、ある日本のYouTubeチャンネルの動画音声を文字起こししたものです。ただし、順番は段落ごとにランダムになっています\n文章の内容から、以下の情報を見つけ出し、返しなさい\n\n- チャンネル名（または話し手の名前）\n- チャンネルのジャンル\n- 話し手の出身地（日本の都道府県単位）\n- 話し口調から推定される方言の地方\n\nわからない項目は不明で構いません。\n最終的な回答は<answer></answer>の中に一行づつ改行して答えなさい。\n\n以下、動画の文字起こしです。\n\n\n---\n\n"

            prompt += segment
            prompt += "\n\n---\n\n\n<｜Assistent｜>\n<think>\n"

            result = self.generate(prompt)
            result = result[result.index("<｜Assistent｜>"):]

            summaries.append(result)

        return summaries

    def generate(self, prompt: str) -> str:
        device = self.llama.device

        tokenized = self.llama_tokenizer(prompt, return_tensors="pt")
        input_ids = tokenized.input_ids.to(device=device)
        attention_mask = tokenized.attention_mask.to(device=device)

        output = self.llama.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=1024,
            pad_token_id=self.llama_tokenizer.eos_token_id,
        )

        decoded = self.llama_tokenizer.batch_decode(output, skip_special_tokens=True)[0]

        return decoded

    def summarize(self, paths: list[str]) -> tuple[str, list[str]]:
        transcribes = [self._transcribe(path) for path in paths]
        text = reduce(lambda p, c: p + "\n\n" + c, transcribes)
        return text, self._summarize_text(text)