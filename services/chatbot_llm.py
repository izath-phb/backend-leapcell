import requests
import os

HF_API_URL = "https://api-inference.huggingface.co/models/izath/chatbot"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def ask_llm(prompt: str):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 64,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    response = requests.post(
        HF_API_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(response.text)

    result = response.json()

    # HF output format
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]

    return str(result)
