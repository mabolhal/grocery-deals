# Grocery Deals; Save This Week

This project is a FastAPI application that integrates with a Telegram bot to provide users stores near them that have the best deals for the week. The bot allows users to send search queries, which are processed by the FastAPI application, and the deals are returned to the user in a formatted message. This project is in progress.

## Features

- **Telegram Bot Integration**: Communicates with users via Telegram.
- **Product Search**: Searches for products using the Backflipp API based on user queries.
- **Unique Merchant Filtering**: Returns the most relevant product from unique merchants.
- **Gemini API Integration**: Forwards search results to the Gemini API for additional processing and receives a JSON response.

## Configuration

Before running the application, you need to set up the configuration file. Create a `config.py` file with the following content:

## config.py
Telegram Bot Token
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
Ngrok URL
NGROK_URL = "YOUR_NGROK_URL"
Gemini API Token
GEMINI_API_TOKEN = "YOUR_GEMINI_API_TOKEN"



## Running the Application

1. **Start ngrok**: To expose your local server to the internet, run ngrok on the port your FastAPI app is running (default is 8000):

   ```bash
   ngrok http 8000
   ```

2. **Run the FastAPI Application**: Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn app:app --reload
   ```

3. **Set the Webhook for Telegram**: Use the ngrok URL to set the webhook for your Telegram bot:

   ```bash
   curl -X POST "https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/setWebhook?url=YOUR_NGROK_URL/webhook"
   ```

4. **Interact with the Bot**: Send a message to your Telegram bot with a search query, and the bot will respond with the search results.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.