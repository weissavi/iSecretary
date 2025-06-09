
import requests
import base64
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# קריאת קובץ הקונפיגורציה המאוחד
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

API_KEY = config["api_key"]
MODEL = config["model"]

OPEN_ROUTER_URL = config["open_router_url"]




IMAGE_PATH = "screenshot.png"  # שים כאן את התמונה שצולמה מהטלפון


with open("prompt.txt", "r", encoding="utf-8") as f:
    prompttext = f.read()

PROMPT = prompttext

# קריאה לקובץ תמונה והמרה ל-base64
with open(IMAGE_PATH, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# בניית בקשת API
data = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}}
            ]
        }
    ]
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# שליחת הבקשה
response = requests.post(OPEN_ROUTER_URL, headers=headers, json=data)

# הצגת התוצאה
result = response.json()
if "choices" not in result:
    print("❌ No valid response from model. Raw response:")
    print(result)
    exit(1)

print(result["choices"][0]["message"]["content"])
