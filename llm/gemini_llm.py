# llm/gemini_llm.py  (PRODUCTION-READY WITH QUOTA HANDLING)

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

def call_llm(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 1000
            }
        )

        text = response.text

        if not text:
            raise ValueError("Gemini returned empty response")

        return text

    except Exception as e:
        err = str(e)

        # Detect quota error explicitly
        if "RESOURCE_EXHAUSTED" in err or "429" in err:
            return "LLM_QUOTA_EXHAUSTED"

        return f"LLM_ERROR: {err}"
