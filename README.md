# Penny Crypto Bot 🤖💰

A Telegram bot with ChatGPT integration for cryptocurrency assistance and general AI conversations.

## Features

- 🤖 ChatGPT integration for intelligent responses
- 📱 Telegram bot interface
- 🔒 Secure API key management with environment variables
- ⚡ Real-time message handling with typing indicators

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/EgeUnlu35/penny_crypto_bot.git
   cd penny_crypto_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Replace the placeholder values with your actual API keys:
     - `BOT_TOKEN`: Get from [@BotFather](https://t.me/botfather) on Telegram
     - `OPENAI_API_KEY`: Get from [OpenAI Platform](https://platform.openai.com/)

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Usage

- Send `/start` to initialize the bot
- Send any text message to get AI-powered responses
- The bot will show typing indicators while processing your requests

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram Bot Token from BotFather | Yes |
| `OPENAI_API_KEY` | OpenAI API Key for ChatGPT | Yes |

## Project Structure

```
.
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env               # Your actual environment variables (not in git)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Future Features

- 🔮 Cryptocurrency price tracking
- 📊 Portfolio management
- 🌐 Sei Network integration
- 💎 DeFi protocol interactions
- 📈 Trading signals and analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Security

⚠️ **Never commit your actual API keys to version control!** 

The `.env` file is excluded from git commits to protect your sensitive information.
