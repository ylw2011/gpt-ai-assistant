from prompt import Prompt

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
system_prompt = "扮演一個女性導覽人員。參考下列內容，會用熱情且積極的語氣回答問題："

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-4o-mini")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 0))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default = 0.5))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default = 0.6))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 240))
        global system_prompt
        with open("kw.txt", "r", encoding="utf-8") as f:
            for line in f:
                system_prompt += line.strip()  # 去掉每行的換行

    def get_response(self):
        global system_prompt
        response = openai.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": self.prompt.generate_prompt()}
        ],
        temperature=self.temperature,
        frequency_penalty=self.frequency_penalty,
        presence_penalty=self.presence_penalty,
        max_tokens=self.max_tokens
        )
        return response.choices[0].message.content.strip()

    def add_msg(self, text):
        self.prompt.add_msg(text)