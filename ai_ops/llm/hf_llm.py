import requests

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": "Bearer hf_dummy_free"}

def call_llm(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500, "temperature": 0.2}
    }

    res = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=40)
    data = res.json()

    if isinstance(data, list):
        return data[0].get("generated_text", "")
    return str(data)
