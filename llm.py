import logging
from anthropic import Anthropic
import random
import instructor
from pydantic import BaseModel

from config import CONFIGS

CLAUDE = CONFIGS['CLAUDE']
client = instructor.from_anthropic(Anthropic(api_key=CLAUDE))

logging.basicConfig(filename='scheduler.log', level=logging.INFO)


class Summary(BaseModel):
    content: str


def get_prompt(cnt, words):
    ws = random.sample(words, 10) if len(words) > 10 else words
    base_msg = f"我今天學了{cnt}個法語單詞！"
    if cnt >= 10:
        return base_msg + f"我已經達到我的目標！請幫我複習一些這些單詞：{ws}。"
    else:
        return base_msg + f"請幫我複習這些單詞：{ws}。然後請鼓勵我學習更多的法語單詞。"


def get_system_prompt(cnt: int) -> str:
    if cnt >= 10:
        return (f"The user works in a all-French environment and is supposed to learn 10 French words a day. And he "
                f"has learnt {cnt} words today. Please simply review his selected words and encourage him to learn "
                f"more. USE traditional Chinese!")
    else:
        return ("The user has not reached his goal of learning 10 French words today. Please review his past selected "
                "words and encourage him to reach his goal immediately. USE traditional Chinese!")


def get_user_prompt(cnt: int, words: list[str]) -> str:
    if cnt == 10:
        return f"我已經達到我的目標！請幫我複習一些這些單詞：{words}。"
    elif cnt == 5:
        return f"不幸的是，我今天沒有達到我的目標。請幫我複習這些過去的單詞：{words}"
    else:
        logging.error(f"Invalid count: {cnt}")
        raise ValueError(f"Invalid count: {cnt}")


def summarize_day(cnt: int, words: list[str]) -> str:
    user_prompt = get_user_prompt(cnt, words)
    system_prompt = get_system_prompt(cnt)
    print("prompt:", user_prompt)
    resp = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=700,
        temperature=0.8,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": user_prompt
        }],
        response_model=Summary
    )
    assert isinstance(resp, Summary)
    return resp.content
