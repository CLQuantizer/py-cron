import anthropic
import random
import time
from typing import List
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

# Your Telegram bot token
CLAUDE = config['CLAUDE']

client = anthropic.Anthropic(api_key=CLAUDE)

get_random_words = lambda words: random.sample(words, 10) if len(words) > 10 else words

def get_prompt(cnt, words):
    words = get_random_words(words)
    base_msg = f"我今天學了{cnt}個法語單詞！"
    if cnt >= 10:
        return base_msg + f"我已經達到我的目標！請幫我複習一些這些單詞：{words}。"
    else:
        return base_msg + f"請幫我複習這些單詞：{words}。然後請鼓勵我學習更多的法語單詞。"


def generate_encouragement(cnt: int, words: list[str]) -> str:
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        try:
            prompt = get_prompt(cnt, words)
            print("prompt:", prompt)
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=500,
                temperature=0.8,
                system="The user is supposed to learn 10 French words a day. "
                       "He works in a all-French environment. Please speak to him only in Traditional Chinese. "
                       "Don't reply too long.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            print(message.content[0])
            return message.content[0].text
        except Exception as e:
            attempt += 1
            if attempt == max_attempts:
                raise e
            print(f"Attempt {attempt} failed. Retrying...")
            time.sleep(2)  # Wait for 2 seconds before retrying

    # This line should never be reached, but it's here for completeness
    raise Exception("Failed to generate encouragement after maximum attempts")