from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import requests
from urllib.parse import urlencode
import json
from config import TELEGRAM_BOT_TOKEN, NGROK_URL, GEMINI_API_TOKEN

app = FastAPI()
token = TELEGRAM_BOT_TOKEN
grok_url = NGROK_URL
gemini_token = GEMINI_API_TOKEN

@app.get("/search")
async def search_flipp(
    q: str = Query(..., description="Search word")  # Description updated
):
    # Validate that q is a single word
    print(q)
    if ' ' in q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' must be a single word.")

    base_url = "https://backflipp.wishabi.com/flipp/items/search"
    
    params = {
        "q": q,
        "postal_code": "H2J1N2",
        "locale": "en-ca",
        "limit": 10,
    }
    
    full_url = f"{base_url}?{urlencode(params)}"
    print("Full URL:", full_url)  # Print the full URL
    
    try:
        print(params)
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        # Extracting the desired information
        data = response.json()
        extracted_items = [
            {
                "current_price": item["current_price"],
                "name": item["name"],
                "image_url": item["image_url"],
                "merchant": item["merchant"],
            }
            for item in data["ecom_items"]
        ]

        # Print the extracted list of dictionaries
        return extracted_items
         
    except requests.RequestException as e:
        return {"error": str(e)}

async def forward_to_gemini(items):
    # Replace with the actual Gemini API endpoint
    gemini_url = "https://api.gemini.com/v1/your_endpoint"  # Update with the correct endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_TOKEN}"  # Replace with your Gemini API token
    }

    
    # Send the filtered items to Gemini
    response = requests.post(gemini_url, headers=headers, json={"items": items, "additional_info":""})
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()  # Return the response from Gemini

@app.post("/webhook")
async def webhook(update: dict):
    # Process the incoming update from Telegram
    chat_id = update["message"]["chat"]["id"]
    message_text = update["message"]["text"]

    search_response = await search_flipp(q=message_text) 
    # Here you can process the message and respond accordingly
    response_text = f"You said: {message_text}"

    print(response_text)
    # Send a response back to the Telegram chat
    send_message(chat_id, response_text)

    return JSONResponse(content={"status": "ok"})

def send_message(chat_id: int, text: str):
      # Replace with your bot's token
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 

