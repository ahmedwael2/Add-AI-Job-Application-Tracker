from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Say hello in one sentence"}],
    max_tokens=50
)

print(response.choices[0].message.content)