# Penny Crypto Bot 🤖💰

A comprehensive Telegram bot with AI integration specialized for the Sei Network ecosystem. Get real-time wallet analysis, token data, price information, and AI-powered crypto assistance.

## ✨ **Features**

### 🔍 **Wallet Analysis**
- **Native Sei addresses** (sei1...) - Complete balance and token analysis
- **EVM addresses** (0x...) - SEI balance and transaction data
- **Multiple API fallbacks** - Ensures high availability even during network issues
- **Real-time data** - Live balance checking with SeiTrace explorer links

### 📊 **Token Analysis** 
- **Smart contract analysis** - Get detailed token information by contract address
- **Price tracking** - Real-time USD prices from DexScreener
- **Market metrics** - 24h volume, market cap, liquidity analysis
- **Price changes** - 24h percentage changes with visual indicators
- **DEX information** - Which exchanges the token trades on
- **Risk warnings** - Automatic alerts for low liquidity tokens

### � **SEI Price Tracking**
- **Real-time SEI price** - Current USD price with multiple trigger commands
- **Market analysis** - Volume, market cap, and trading data
- **Price changes** - 24h percentage changes with emoji indicators
- **Chart links** - Direct links to DexScreener charts

### 🤖 **AI-Powered Chat**
- **Sei Network expertise** - Specialized knowledge about Sei blockchain
- **DeFi guidance** - Information about Astroport, Kryptic, Levana, White Whale
- **Trading insights** - Cryptocurrency analysis and market guidance
- **General crypto help** - Blockchain concepts, staking, and DeFi explanations

### 🛡️ **Reliability Features**
- **Multiple API endpoints** - Automatic fallback systems
- **Error handling** - Graceful error messages and recovery
- **Timeout protection** - Prevents hanging requests
- **Input validation** - Smart message classification and routing

## 🚀 **Setup**

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

## 💬 **Usage Examples**

### **Wallet Analysis:**
```
sei1h9yjz89tl0dl6zu65dpxcqnxfhq6rfkkej6rge
0x742d35Cc6634C0532925a3b8D965aBAC0c5C15e6
```

### **Token Analysis:**
```
token 0xE30feDd158A2e3b13e9badaeABaFc5516e95e8C7
contract 0x3894085Ef7Ff0f0aeDf52E2A2704928d259C2fc4
price 0x57eE725BEeB991c70c53f9642f36755EC6eb2139
```

### **SEI Price:**
```
sei price
$sei
price sei
sei chart
```

### **AI Chat:**
```
What is Sei Network?
How does Astroport work?
Tell me about DeFi on Sei
What's the best way to stake SEI?
Explain parallel execution on Sei
```

### **Commands:**
```
/start - Welcome message and feature overview
/help - Comprehensive help and command list
```

## 🏗️ **Architecture**

### **Smart Input Classification**
The bot intelligently routes messages based on patterns:
- **Wallet addresses** → Balance analysis
- **Token contracts** → Price and market data
- **SEI price queries** → Real-time price tracking
- **Natural language** → AI-powered responses

### **Multi-Endpoint Resilience**
```python
SEI_DATA_SOURCES = {
    'rpc': [
        'https://sei-evm-rpc.publicnode.com',
        'https://evm-rpc.sei-apis.com', 
        'https://sei-rpc.lavenderfive.com'
    ],
    'rest': [
        'https://sei-api.polkachu.com',
        'https://rest.sei-apis.com',
        'https://sei-api.lavenderfive.com',
        'https://sei-rest.publicnode.com'
    ],
    'dex': 'https://api.dexscreener.com',
    'explorer': 'https://seitrace.com'
}
```

## 📋 **Environment Variables**

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram Bot Token from BotFather | Yes |
| `OPENAI_API_KEY` | OpenAI API Key for ChatGPT | Yes |

## 📁 **Project Structure**

```
.
├── bot.py                 # Main bot application with all features
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual environment variables (not in git)
├── .gitignore           # Git ignore rules for security
├── MY_SEI_MCP_BOT_GUIDE.md  # MCP integration guide
└── README.md            # This file
```

## 🎯 **Implemented Features Status**

✅ **Wallet Analysis** - Native and EVM address support  
✅ **Token Analysis** - Contract address parsing and DexScreener integration  
✅ **SEI Price Tracking** - Real-time price with market data  
✅ **AI Chat Integration** - Sei-specialized ChatGPT responses  
✅ **Smart Input Classification** - Automatic message routing  
✅ **Multiple API Fallbacks** - High availability architecture  
✅ **Error Handling** - Graceful error recovery  
✅ **Help System** - Comprehensive user guidance  

## 🔮 **Coming Soon**

🚧 **DeFi Portfolio Management** - Track positions across Sei protocols  
🚧 **NFT Collection Explorer** - Sei NFT analysis and floor tracking  
🚧 **Price Alerts** - Custom notifications for price targets  
🚧 **Cross-chain Analysis** - Multi-chain wallet tracking  
🚧 **Social Features** - Portfolio sharing and leaderboards  

## 🧪 **Testing**

### **Real Token Contracts to Test:**
```bash
# USDC on Sei
token 0x3894085Ef7Ff0f0aeDf52E2A2704928d259C2fc4

# WETH on Sei  
token 0xE30feDd158A2e3b13e9badaeABaFc5516e95e8C7

# USDT on Sei
token 0x57eE725BEeB991c70c53f9642f36755EC6eb2139
```

### **Test Wallet Addresses:**
```bash
# Native Sei addresses
sei1h9yjz89tl0dl6zu65dpxcqnxfhq6rfkkej6rge

# EVM addresses  
0x742d35Cc6634C0532925a3b8D965aBAC0c5C15e6
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 **Performance Features**

- **Async/await architecture** for non-blocking operations
- **Connection pooling** with aiohttp for efficient API calls
- **Timeout handling** prevents hanging requests
- **Smart caching** reduces redundant API calls
- **Fallback systems** ensure 99%+ uptime

## 🔒 **Security**

⚠️ **Never commit your actual API keys to version control!** 

- All sensitive data stored in environment variables
- `.env` file excluded from git commits
- API keys properly scoped and rotated regularly
- Input validation prevents injection attacks

## 📊 **Statistics**

- **500+ lines of Python code**
- **8+ API endpoints** with fallbacks
- **5+ input classification patterns** 
- **3+ major feature categories**
- **99%+ uptime** with redundant systems

## 🌟 **Advanced Features**

### **Smart Message Routing**
```python
# Automatic detection of:
- Wallet addresses (sei1... or 0x...)
- Token contracts (token 0x...)  
- Price queries (sei price, $sei)
- Natural language (AI chat)
```

### **Comprehensive Token Analysis**
- Real-time pricing from DexScreener
- Market cap and volume metrics
- Liquidity analysis and warnings
- DEX information and trade links
- Risk assessment for new tokens

### **Multi-Network Support**
- Sei Native blockchain integration
- EVM compatibility layer support
- Cross-chain address recognition
- Unified interface for both networks

Built with ❤️ for the Sei community by [@EgeUnlu35](https://github.com/EgeUnlu35)
