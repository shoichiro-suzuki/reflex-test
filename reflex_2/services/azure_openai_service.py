import os
from dotenv import load_dotenv
from openai import AzureOpenAI


class AzureOpenAIService:
    """
    Azure OpenAI サービスへの接続・応答取得を管理するクラス。
    """

    def __init__(self):
        load_dotenv()
        self.os = os
        self.client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("OPENAI_API_BASE"),
        )

    def get_openai_response_4o(self, messages, max_tokens, temperature=0.0):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
        )
        answer = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return answer, input_tokens, output_tokens

    def get_openai_response_o1(self, messages, max_tokens):
        response = self.client.chat.completions.create(
            model="o1",
            messages=messages,
            max_completion_tokens=max_tokens,
        )
        answer = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return answer, input_tokens, output_tokens

    def get_openai_response_o3(self, messages, max_tokens):
        response = self.client.chat.completions.create(
            model="o3-mini",
            messages=messages,
            max_completion_tokens=max_tokens,
        )
        answer = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return answer, input_tokens, output_tokens

    def get_openai_response_gpt41mini(self, messages, max_tokens):
        response = self.client.chat.completions.create(
            messages=messages,
            max_completion_tokens=max_tokens,
            temperature=0.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            model="gpt-4.1-mini",
        )
        answer = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return answer, input_tokens, output_tokens

    def get_openai_response_gpt41nano(self, messages, max_tokens):
        response = self.client.chat.completions.create(
            messages=messages,
            max_completion_tokens=max_tokens,
            temperature=0.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            model="gpt-4.1-nano",
        )
        answer = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return answer, input_tokens, output_tokens

    def text_to_speech(
        self,
        text,
        output_path="output_audio.mp3",
        voice="alloy",
        model="gpt-4o-mini-tts",
        instructions="明るく元気な声で話してください",
    ):
        try:
            response = self.client.audio.speech.create(
                model=model,
                input=text,
                voice=voice,
            )
            with open(output_path, "wb") as f:
                f.write(response.content)
            return True
        except Exception as e:
            print(f"音声合成エラー: {e}")
            return False

    def speech_to_text(self, audio_file_path, model="gpt-4o-transcribe"):
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                )
            return response.text
        except Exception as e:
            print(f"音声認識エラー: {e}")
            return None
