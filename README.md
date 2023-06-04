# Respect Bot
## Description
Write me
Test

## How To Run
### Manual
1. Fill .env file with OpenAI and Telegram API keys.
2. Install dependencies.
```bash
pip install -r requirements.txt
```
3. Run script
```bash
python main.py
```
```bash
cd Documents/GitHub/BOT_RESPECTO
source env/bin/activate
python3 src/main.py
```
### Docker (Not Ready)
1. Fill .env file with OpenAI and Telegram API keys.
2. Build docker image
```bash
docker build -t bot_respect .
```
3. Run image
```bash
docker run -e OPENAI_API_KEY=<YOUR_OPENAI_KEY> -e TELEGRAM_API_KEY=<YOUR_TELEGRAM_KEY> bot_respect
```

