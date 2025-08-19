# Building Your Own Telegram Sei MCP Bot

## 🎯 Project Overview

This guide shows how to create your own **Telegram Sei MCP (Model Context Protocol) Bot** by leveraging the architecture and patterns from the Seiva Bot project.

### **What You'll Build**
- **Telegram Bot**: Conversational interface for Sei Network
- **MCP Integration**: Advanced AI agent capabilities with structured tools
- **Blockchain Integration**: Real-time Sei Network data
- **Multi-Modal Features**: Wallet tracking, token analysis, DeFi interactions
- **Extensible Architecture**: Easy to add new features and integrations

## 🏗️ **Architecture Overview**

```
Telegram Input → MCP Server → AI Agent with Tools → Blockchain APIs → Response
                     ↓
              [Tool Collection]
              ├── Wallet Checker
              ├── Token Analyzer  
              ├── DeFi Tracker
              ├── NFT Explorer
              └── Custom Tools
```

## 📋 **Prerequisites**

### **Required Knowledge**
- JavaScript/TypeScript basics
- REST API integration
- Telegram Bot API
- Model Context Protocol (MCP)
- Blockchain fundamentals

### **Tools & Services**
- **MCP Server**: Claude Desktop or compatible MCP client
- **AI Provider**: OpenAI, Anthropic, or local models
- **Automation Platform**: n8n (optional), custom Node.js/Python server
- **Telegram Bot Token**: From @BotFather
- **Hosting**: Vercel, Railway, Heroku, or VPS

### **Language Options**
- **Python**: Recommended for rapid prototyping, rich ML/AI ecosystem
- **TypeScript/Node.js**: Great for full-stack JavaScript developers
- **Both approaches are fully supported in this guide**

## 🚀 **Implementation Options**

### **Option 1: Pure Python MCP Approach (Recommended)**

Create a dedicated MCP server with Sei-specific tools using Python:

```python
# mcp_sei_server.py
import asyncio
import json
from mcp import Server, ListToolsRequest, CallToolRequest, Tool
from mcp.server.models import InitializationOptions
import aiohttp
from typing import Any, Sequence

class SeiMCPServer:
    def __init__(self):
        self.server = Server("sei-network-tools")
        self.setup_tools()
    
    def setup_tools(self):
        @self.server.list_tools()
        async def handle_list_tools(request: ListToolsRequest) -> list[Tool]:
            return [
                Tool(
                    name="check_sei_wallet",
                    description="Check SEI wallet balance and info",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "address": {"type": "string", "description": "Wallet address"}
                        },
                        "required": ["address"]
                    }
                ),
                Tool(
                    name="analyze_sei_token",
                    description="Analyze Sei token metrics and data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "contract": {"type": "string", "description": "Token contract address"}
                        },
                        "required": ["contract"]
                    }
                ),
                Tool(
                    name="get_defi_positions",
                    description="Get DeFi positions for a wallet",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "wallet": {"type": "string", "description": "Wallet address"}
                        },
                        "required": ["wallet"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(request: CallToolRequest) -> Sequence[Any]:
            if request.params.name == "check_sei_wallet":
                return await self.check_sei_wallet(request.params.arguments["address"])
            elif request.params.name == "analyze_sei_token":
                return await self.analyze_sei_token(request.params.arguments["contract"])
            elif request.params.name == "get_defi_positions":
                return await self.get_defi_positions(request.params.arguments["wallet"])
            else:
                raise ValueError(f"Unknown tool: {request.params.name}")
    
    async def check_sei_wallet(self, address: str):
        # Implementation coming next...
        pass

if __name__ == "__main__":
    server = SeiMCPServer()
    asyncio.run(server.server.run())
```

### **Option 2: TypeScript MCP Approach**

Create a dedicated MCP server with Sei-specific tools:

```typescript
// mcp-sei-server.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server(
  {
    name: 'sei-network-tools',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Tool: Check Sei Wallet Balance
server.setRequestHandler(ToolCallRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  switch (name) {
    case 'check_sei_wallet':
      return await checkSeiWallet(args.address);
    case 'analyze_sei_token':
      return await analyzeSeiToken(args.contract);
    case 'get_sei_defi_positions':
      return await getDeFiPositions(args.wallet);
    // Add more tools...
  }
});
```

### **Option 3: Python Telegram Bot with MCP Integration**

Use Python for Telegram handling and MCP for AI logic:

```python
# telegram_sei_bot.py
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import aiohttp
import json
from mcp_client import MCPClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeiTelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.mcp_client = MCPClient()
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🌊 Welcome to Sei MCP Bot!\n\n"
            "Send me:\n"
            "• A wallet address (0x... or sei1...)\n"
            "• 'token 0x...' for token analysis\n"
            "• 'portfolio' for DeFi positions\n"
            "• Any question about Sei Network"
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        chat_id = update.message.chat_id
        
        try:
            # Classify and route message through MCP
            response = await self.mcp_client.process_message(user_message)
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text("Sorry, something went wrong. Please try again.")
    
    def run(self):
        self.app.run_polling()

if __name__ == "__main__":
    bot = SeiTelegramBot("YOUR_TELEGRAM_TOKEN")
    bot.run()
```

### **Option 4: Hybrid n8n + Python MCP**

Use n8n for Telegram handling, Python MCP for AI logic:

```javascript
// n8n workflow with Python MCP integration
{
  "name": "Telegram to Python MCP Bridge",
  "nodes": [
    {
      "name": "Telegram Trigger",
      "type": "n8n-nodes-base.telegramTrigger"
    },
    {
      "name": "Python MCP Server Call",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8000/mcp-agent",
        "method": "POST",
        "body": {
          "message": "={{$json.message.text}}",
          "chat_id": "={{$json.message.chat.id}}"
        }
      }
    }
  ]
}
```

## 🛠️ **Core Tools to Implement**

### **1. Wallet Analysis Tool**

**Python Implementation:**
```python
import aiohttp
import asyncio
from decimal import Decimal

async def check_sei_wallet(address: str):
    """Check SEI wallet balance using RPC - Python version"""
    
    rpc_payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://sei-evm-rpc.publicnode.com",
            json=rpc_payload,
            headers={"Content-Type": "application/json"}
        ) as response:
            data = await response.json()
            
    # Convert Wei to SEI
    wei_balance = int(data["result"], 16)
    sei_balance = Decimal(wei_balance) / Decimal(10**18)
    
    # Hardcoded SEI price (you can fetch from CoinGecko)
    sei_usd_price = 0.32
    usd_value = float(sei_balance) * sei_usd_price
    
    return [{
        "type": "text",
        "text": f"💰 **Wallet Balance**\n"
                f"• SEI: {sei_balance:.4f}\n"
                f"• USD: ${usd_value:.2f}\n\n"
                f"🔗 [View on SeiTrace](https://seitrace.com/account/{address})"
    }]

# Input classification for Python
import re

def classify_input(message: str):
    """Classify user input - Python version derived from Seiva's JS logic"""
    
    patterns = {
        'wallet': r'^(sei1[a-z0-9]{38}|0x[a-fA-F0-9]{40})$',
        'token': r'^token\s+(0x[a-fA-F0-9]{40})$',
        'defi': r'^(positions|portfolio|defi)\s*(.*)?$',
        'nft': r'^(nft|nfts|collection)\s*(.*)?$',
        'help': r'^(/help|help|/start)$'
    }
    
    message_lower = message.strip().lower()
    
    for msg_type, pattern in patterns.items():
        match = re.match(pattern, message_lower, re.IGNORECASE)
        if match:
            return {
                'type': msg_type,
                'data': match.groups() if match.groups() else None,
                'address': match.group(1) if msg_type in ['wallet', 'token'] else None
            }
    
    return {'type': 'general', 'data': None, 'address': None}
```

**TypeScript Implementation:**
```typescript
async function checkSeiWallet(address: string) {
  // Reuse Seiva's pattern
  const rpcResponse = await fetch('https://sei-evm-rpc.publicnode.com', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      method: 'eth_getBalance',
      params: [address, 'latest'],
      id: 1
    })
  });
  
  const { result } = await rpcResponse.json();
  const balance = BigInt(result) / BigInt(10**18);
  
  return {
    content: [{
      type: 'text',
      text: `Wallet ${address} has ${balance} SEI tokens`
    }]
  };
}
```

### **2. Token Intelligence Tool**

**Python Implementation:**
```python
async def analyze_sei_token(contract: str):
    """Analyze Sei token using DexScreener and SeiTrace APIs"""
    
    # Parallel API calls like Seiva
    async with aiohttp.ClientSession() as session:
        dex_task = session.get(f"https://api.dexscreener.com/latest/dex/tokens/{contract}")
        meta_task = session.get(f"https://seitrace.com/token/{contract}")
        
        dex_response, meta_response = await asyncio.gather(dex_task, meta_task)
        dex_data = await dex_response.json()
        meta_data = await meta_response.json()
    
    # Validate it's on Sei Network
    pairs = dex_data.get('pairs', [])
    if not pairs:
        return [{"type": "text", "text": "❌ Token not found or not on Sei Network"}]
    
    pair = pairs[0]
    chain_id = str(pair.get('chainId', '')).lower()
    
    if 'sei' not in chain_id:
        return [{
            "type": "text", 
            "text": "❌ Sorry, this bot only supports tokens on the *Sei Network*.\n"
                   "The address appears to be on a different chain."
        }]
    
    # Extract token info (following Seiva's formatting logic)
    token = pair.get('baseToken', {})
    name = token.get('name', 'Unknown')
    symbol = token.get('symbol', '')
    
    price = float(pair.get('priceUsd', 0))
    market_cap = float(pair.get('marketCap', 0))
    volume_24h = float(pair.get('volume', {}).get('h24', 0))
    liquidity = float(pair.get('liquidity', {}).get('usd', 0))
    
    # Price change
    price_change_1h = float(pair.get('priceChange', {}).get('h1', 0))
    change_str = f"+{price_change_1h:.2f}%" if price_change_1h > 0 else f"{price_change_1h:.2f}%"
    
    # Format large numbers
    def format_big(num):
        if num >= 1e9:
            return f"{num/1e9:.2f} B"
        elif num >= 1e6:
            return f"{num/1e6:.2f} M"
        elif num >= 1e3:
            return f"{num/1e3:.2f} K"
        return f"{num:.2f}"
    
    # Build response
    analysis = f"""📊 **{name}** ({symbol})
```
{contract}
```
• Price       : ${price:.7f}
• Market Cap  : ${format_big(market_cap)}
• Change 1h   : {change_str}
• Volume 24h  : ${format_big(volume_24h)}
• Liquidity   : ${format_big(liquidity)}

🔗 **Swap on DragonSwap:** [Open](https://dragonswap.app/swap?inputCurrency=SEI&outputCurrency={contract})"""
    
    return [{"type": "text", "text": analysis}]
```

**TypeScript Implementation:**
```typescript
async function analyzeSeiToken(contract: string) {
  // Parallel API calls like Seiva
  const [dexData, metaData] = await Promise.all([
    fetch(`https://api.dexscreener.com/latest/dex/tokens/${contract}`),
    fetch(`https://seitrace.com/token/${contract}`)
  ]);
  
  const tokenInfo = {
    price: dexData.pairs?.[0]?.priceUsd,
    volume24h: dexData.pairs?.[0]?.volume?.h24,
    marketCap: dexData.pairs?.[0]?.marketCap,
    // Add more metrics...
  };
  
  return {
    content: [{
      type: 'text', 
      text: `Token Analysis: ${JSON.stringify(tokenInfo, null, 2)}`
    }]
  };
}
```

### **3. DeFi Portfolio Tool**

**Python Implementation:**
```python
async def get_defi_positions(wallet: str):
    """Get DeFi positions across Sei protocols"""
    
    # Sei DeFi protocols
    protocols = [
        {'name': 'astroport', 'api': 'https://api.astroport.fi'},
        {'name': 'kryptic', 'api': 'https://api.kryptic.fi'},
        {'name': 'levana', 'api': 'https://api.levana.finance'},
        {'name': 'white-whale', 'api': 'https://api.whitewhale.money'}
    ]
    
    positions = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for protocol in protocols:
            task = fetch_protocol_position(session, wallet, protocol)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for protocol, result in zip(protocols, results):
            if isinstance(result, Exception):
                continue
            if result:
                positions.append({
                    'protocol': protocol['name'],
                    'value': result.get('total_value', 0),
                    'positions': result.get('positions', [])
                })
    
    if not positions:
        return [{
            "type": "text",
            "text": "🏦 **DeFi Portfolio**\n\nNo active positions found on supported protocols."
        }]
    
    # Format positions
    total_value = sum(p['value'] for p in positions)
    position_lines = [f"• {p['protocol'].title()}: ${p['value']:.2f}" for p in positions]
    
    portfolio_text = f"""🏦 **DeFi Portfolio**
    
**Total Value:** ${total_value:.2f}

{chr(10).join(position_lines)}

💡 *Tracking: Astroport, Kryptic, Levana, White Whale*"""
    
    return [{"type": "text", "text": portfolio_text}]

async def fetch_protocol_position(session: aiohttp.ClientSession, wallet: str, protocol: dict):
    """Fetch position from a specific protocol"""
    try:
        # This would need protocol-specific implementation
        async with session.get(f"{protocol['api']}/positions/{wallet}") as response:
            if response.status == 200:
                return await response.json()
    except Exception as e:
        print(f"Error fetching {protocol['name']}: {e}")
    return None
```

**TypeScript Implementation:**
```typescript
async function getDeFiPositions(wallet: string) {
  // Integrate with Sei DeFi protocols
  const protocols = [
    'astroport', 'kryptic', 'levana', 'white-whale'
  ];
  
  const positions = await Promise.all(
    protocols.map(protocol => fetchProtocolPosition(wallet, protocol))
  );
  
  return {
    content: [{
      type: 'text',
      text: `DeFi Portfolio: ${formatPositions(positions)}`
    }]
  };
}
```

### **4. NFT Explorer Tool**

**Python Implementation:**
```python
async def explore_sei_nfts(wallet: str):
    """Query Sei NFT collections for a wallet"""
    
    # Sei NFT data sources
    nft_apis = [
        f"https://api.sei-nft-indexer.com/wallet/{wallet}",
        f"https://api.stargaze.zone/graphql"  # If Sei NFTs are indexed here
    ]
    
    nft_collections = []
    
    async with aiohttp.ClientSession() as session:
        for api_url in nft_apis:
            try:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Process NFT data based on API response format
                        if 'nfts' in data:
                            nft_collections.extend(data['nfts'])
            except Exception as e:
                print(f"Error fetching NFTs from {api_url}: {e}")
    
    if not nft_collections:
        return [{
            "type": "text",
            "text": "🖼️ **NFT Holdings**\n\nNo NFTs found in this wallet on Sei Network."
        }]
    
    # Group by collection
    collections = {}
    for nft in nft_collections:
        collection = nft.get('collection', 'Unknown')
        if collection not in collections:
            collections[collection] = []
        collections[collection].append(nft)
    
    # Format response
    collection_lines = []
    total_nfts = len(nft_collections)
    
    for collection, nfts in collections.items():
        collection_lines.append(f"• {collection}: {len(nfts)} NFTs")
    
    nft_text = f"""🖼️ **NFT Holdings**

**Total NFTs:** {total_nfts}
**Collections:** {len(collections)}

{chr(10).join(collection_lines)}

🔗 *View on Sei NFT Explorer*"""
    
    return [{"type": "text", "text": nft_text}]
```

**TypeScript Implementation:**
```typescript
async function exploreSeiNFTs(wallet: string) {
  // Query Sei NFT collections
  const nftData = await fetch(`https://api.sei-nft-indexer.com/wallet/${wallet}`);
  
  return {
    content: [{
      type: 'text',
      text: `NFT Holdings: ${formatNFTData(nftData)}`
    }]
  };
}
```

## 🔧 **Key Integration Patterns from Seiva**

### **1. Input Classification**

**Python Implementation:**
```python
import re
from typing import Dict, Optional, List

def classify_input(message: str) -> Dict:
    """Classify user input based on Seiva's patterns"""
    
    patterns = {
        'wallet': r'^(sei1[a-z0-9]{38}|0x[a-fA-F0-9]{40})$',
        'token': r'^token\s+(0x[a-fA-F0-9]{40})$',
        'defi': r'^(positions|portfolio|defi)\s*(.*)?$',
        'nft': r'^(nft|nfts|collection)\s*(.*)?$',
        'help': r'^(/help|help|/start)$',
        'general': r'^(?!.*(?:sei1|0x))'
    }
    
    message_clean = message.strip().lower()
    
    for msg_type, pattern in patterns.items():
        match = re.match(pattern, message_clean, re.IGNORECASE)
        if match:
            result = {
                'type': msg_type,
                'original_message': message,
                'address': None,
                'query': None
            }
            
            if msg_type == 'wallet':
                result['address'] = match.group(1)
            elif msg_type == 'token':
                result['address'] = match.group(1)
            elif msg_type == 'general':
                result['query'] = message
                
            return result
    
    return {'type': 'general', 'query': message, 'address': None}

# Example usage
examples = [
    "0x742d35Cc6634C0532925a3b8D97B3cd",
    "token 0x123abc...",
    "portfolio",
    "What's the best way to stake SEI?",
    "/help"
]

for example in examples:
    result = classify_input(example)
    print(f"Input: {example} -> Type: {result['type']}")
```

**TypeScript Implementation:**
```typescript
function classifyInput(message: string) {
  const patterns = {
    wallet: /^(sei1[a-z0-9]{38}|0x[a-fA-F0-9]{40})$/,
    token: /^token\s+(0x[a-fA-F0-9]{40})$/,
    defi: /^(positions|portfolio|defi)\s*(.*)?$/i,
    nft: /^(nft|nfts|collection)\s*(.*)?$/i,
    general: /^(?!.*(?:sei1|0x))/
  };
  
  for (const [type, regex] of Object.entries(patterns)) {
    if (regex.test(message)) {
      return { type, data: message.match(regex) };
    }
  }
  
  return { type: 'general', data: null };
}
```

### **2. Data Source Integration**

**Python Configuration:**
```python
# sei_data_sources.py
from dataclasses import dataclass
from typing import Dict, Any
import aiohttp

@dataclass
class SeiDataSources:
    """Sei Network data source configuration"""
    
    RPC_ENDPOINTS = [
        "https://sei-evm-rpc.publicnode.com",
        "https://evm-rpc.sei-apis.com",
        "https://sei-rpc.polkachu.com"
    ]
    
    REST_ENDPOINTS = [
        "https://sei-api.polkachu.com",
        "https://sei-rest.publicnode.com"
    ]
    
    DEX_API = "https://api.dexscreener.com"
    EXPLORER_API = "https://seitrace.com"
    
    DEFI_APIS = {
        "astroport": "https://api.astroport.fi",
        "kryptic": "https://api.kryptic.fi",
        "levana": "https://api.levana.finance",
        "white_whale": "https://api.whitewhale.money"
    }
    
    NFT_APIS = [
        "https://api.sei-nft-indexer.com",
        "https://nft-api.sei.io"
    ]

class SeiAPIClient:
    """Unified API client for Sei Network data"""
    
    def __init__(self):
        self.sources = SeiDataSources()
    
    async def get_wallet_balance(self, address: str) -> Dict[str, Any]:
        """Get wallet balance with fallback RPC endpoints"""
        
        rpc_payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance", 
            "params": [address, "latest"],
            "id": 1
        }
        
        async with aiohttp.ClientSession() as session:
            for rpc_url in self.sources.RPC_ENDPOINTS:
                try:
                    async with session.post(rpc_url, json=rpc_payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data
                except Exception as e:
                    print(f"RPC {rpc_url} failed: {e}")
                    continue
        
        raise Exception("All RPC endpoints failed")
    
    async def get_token_data(self, contract: str) -> Dict[str, Any]:
        """Get token data from multiple sources"""
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                session.get(f"{self.sources.DEX_API}/latest/dex/tokens/{contract}"),
                session.get(f"{self.sources.EXPLORER_API}/token/{contract}")
            ]
            
            try:
                responses = await asyncio.gather(*tasks)
                dex_data = await responses[0].json() if responses[0].status == 200 else {}
                explorer_data = await responses[1].json() if responses[1].status == 200 else {}
                
                return {
                    "dex": dex_data,
                    "explorer": explorer_data
                }
            except Exception as e:
                print(f"Error fetching token data: {e}")
                return {"dex": {}, "explorer": {}}
```

**TypeScript Configuration:**
```typescript
const SEI_DATA_SOURCES = {
  rpc: 'https://sei-evm-rpc.publicnode.com',
  rest: 'https://sei-api.polkachu.com',
  dex: 'https://api.dexscreener.com',
  explorer: 'https://seitrace.com',
  defi: {
    astroport: 'https://api.astroport.fi',
    kryptic: 'https://api.kryptic.fi'
  }
};
```

### **3. Response Formatting**

**Python Implementation:**
```python
def format_response(data: Dict[str, Any], response_type: str) -> str:
    """Format response based on data type"""
    
    formatters = {
        'wallet': format_wallet_response,
        'token': format_token_response,
        'defi': format_defi_response,
        'nft': format_nft_response,
        'error': format_error_response
    }
    
    formatter = formatters.get(response_type, format_generic_response)
    return formatter(data)

def format_wallet_response(data: Dict[str, Any]) -> str:
    """Format wallet balance response"""
    balance = data.get('balance', 0)
    usd_value = data.get('usd_value', 0)
    address = data.get('address', '')
    
    return f"""💰 **Wallet Balance**
• SEI: {balance:.4f}
• USD: ${usd_value:.2f}

🔗 [View on SeiTrace](https://seitrace.com/account/{address})"""

def format_token_response(data: Dict[str, Any]) -> str:
    """Format token analysis response"""
    name = data.get('name', 'Unknown')
    symbol = data.get('symbol', '')
    price = data.get('price', 0)
    change_24h = data.get('change_24h', 0)
    market_cap = data.get('market_cap', 0)
    
    change_emoji = "📈" if change_24h > 0 else "📉"
    
    return f"""📊 **{name}** ({symbol})
• Price: ${price:.6f}
• 24h Change: {change_emoji} {change_24h:+.2f}%
• Market Cap: ${format_big_number(market_cap)}"""

def format_defi_response(data: Dict[str, Any]) -> str:
    """Format DeFi portfolio response"""
    positions = data.get('positions', [])
    total_value = sum(p.get('value', 0) for p in positions)
    
    if not positions:
        return "🏦 **DeFi Portfolio**\n\nNo active positions found."
    
    position_lines = [
        f"• {p['protocol'].title()}: ${p['value']:.2f}" 
        for p in positions
    ]
    
    return f"""🏦 **DeFi Portfolio**

**Total Value:** ${total_value:.2f}

{chr(10).join(position_lines)}"""

def format_big_number(num: float) -> str:
    """Format large numbers with K/M/B suffixes"""
    if num >= 1e9:
        return f"{num/1e9:.2f}B"
    elif num >= 1e6:
        return f"{num/1e6:.2f}M"
    elif num >= 1e3:
        return f"{num/1e3:.2f}K"
    return f"{num:.2f}"
```

**TypeScript Implementation:**
```typescript
function formatResponse(data: any, type: string) {
  switch (type) {
    case 'wallet':
      return `💰 **Wallet Balance**\n• SEI: ${data.balance}\n• USD: $${data.usdValue}`;
    case 'token':
      return `📊 **${data.name}** (${data.symbol})\n• Price: $${data.price}\n• 24h: ${data.change24h}%`;
    case 'defi':
      return `🏦 **DeFi Portfolio**\n${data.positions.map(p => `• ${p.protocol}: $${p.value}`).join('\n')}`;
  }
}
```

## 📱 **Enhanced Features Beyond Seiva**

### **1. Advanced DeFi Integration**
- **Yield Farming Tracker**: Monitor LP positions across Sei DEXs
- **Staking Rewards**: Track validator rewards and compound strategies
- **Cross-Chain Bridge Monitor**: Alert on bridge transactions

### **2. Trading Intelligence**
- **Price Alerts**: Set custom price notifications
- **MEV Protection**: Detect sandwich attacks
- **Arbitrage Opportunities**: Find profitable trades across DEXs

### **3. Social Features**
- **Portfolio Sharing**: Generate shareable portfolio summaries
- **Leaderboards**: Compare performance with other users
- **Alert Groups**: Community-driven alert channels

### **4. Advanced Analytics**
- **Risk Assessment**: Analyze token risk metrics
- **Whale Tracking**: Monitor large wallet movements
- **Trend Analysis**: Identify emerging tokens and patterns

## 🚀 **Deployment Guide**

### **Step 1: Set Up Python MCP Server**

```bash
# Create new Python MCP project
mkdir sei-mcp-bot
cd sei-mcp-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install mcp aiohttp python-telegram-bot python-dotenv asyncio

# Create requirements.txt
pip freeze > requirements.txt
```

**Project Structure:**
```
sei-mcp-bot/
├── main.py                 # MCP server entry point
├── telegram_bot.py         # Telegram bot handler
├── sei_tools.py           # Sei-specific MCP tools
├── data_sources.py        # API clients and data sources
├── formatters.py          # Response formatting
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # Project documentation
```

**main.py - MCP Server:**
```python
#!/usr/bin/env python3
import asyncio
import os
from mcp import Server
from sei_tools import SeiTools
from config import Config

async def main():
    config = Config()
    server = Server("sei-network-tools")
    sei_tools = SeiTools(config)
    
    # Register all Sei-specific tools
    await sei_tools.register_tools(server)
    
    # Start the MCP server
    async with server:
        await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

**config.py - Configuration:**
```python
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Configuration for Sei MCP Bot"""
    
    # API Keys
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Sei Network Settings
    SEI_RPC_URL: str = os.getenv("SEI_RPC_URL", "https://sei-evm-rpc.publicnode.com")
    SEI_REST_URL: str = os.getenv("SEI_REST_URL", "https://sei-api.polkachu.com")
    
    # External APIs
    DEXSCREENER_API: str = "https://api.dexscreener.com"
    SEITRACE_API: str = "https://seitrace.com"
    
    # Bot Settings
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 30
    CACHE_TTL: int = 300  # 5 minutes
    
    def validate(self):
        """Validate required configuration"""
        if not self.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN is required")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
```

### **Step 2: Set Up TypeScript MCP Server (Alternative)**

```bash
# Create new TypeScript MCP project
npm create mcp-server@latest sei-mcp-bot
cd sei-mcp-bot

# Install additional dependencies
npm install axios telegram-bot-api dotenv
npm install --save-dev @types/node typescript
```

### **Step 3: Configure Telegram Bot (Python)**

**telegram_bot.py:**
```python
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from mcp_client import MCPClient
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeiTelegramBot:
    def __init__(self, config: Config):
        self.config = config
        self.mcp_client = MCPClient()
        self.app = Application.builder().token(config.TELEGRAM_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up Telegram command and message handlers"""
        
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("portfolio", self.portfolio_command))
        
        # Message handlers
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_text = """🌊 **Welcome to Sei MCP Bot!**

I can help you with:
• 💰 **Wallet Analysis**: Send any Sei wallet address
• 📊 **Token Intelligence**: `token 0x...` for detailed analysis  
• 🏦 **DeFi Portfolio**: `portfolio` to see your positions
• 🖼️ **NFT Explorer**: `nft` to view your collections
• 💬 **Sei Q&A**: Ask anything about Sei Network

**Example Commands:**
• `0x742d35Cc6634C0532925a3b8D97B3cd` (wallet)
• `token 0x123...abc` (token analysis)
• `portfolio` (DeFi positions)
• `What's the best DEX on Sei?` (questions)

Try it out! 🚀"""
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """🔧 **Sei MCP Bot Commands**

**Wallet Analysis:**
• Send any Sei address (0x... or sei1...)
• Get balance, USD value, and explorer link

**Token Analysis:**
• `token 0x...` - Detailed token metrics
• Price, volume, market cap, liquidity

**DeFi Portfolio:**
• `portfolio` - Your DeFi positions across protocols
• Tracks Astroport, Kryptic, Levana, White Whale

**NFT Explorer:**
• `nft` or `nfts` - Your NFT collections

**General Questions:**
• Ask anything about Sei Network
• DeFi protocols, staking, airdrops, etc.

Need more help? Just ask! 💬"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def portfolio_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /portfolio command"""
        await update.message.reply_text(
            "🏦 To view your portfolio, please send your wallet address first.\n"
            "Example: `0x742d35Cc6634C0532925a3b8D97B3cd`",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages"""
        user_message = update.message.text
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        
        try:
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=chat_id, action='typing')
            
            # Process message through MCP
            response = await self.mcp_client.process_message(
                message=user_message,
                user_id=user_id,
                chat_id=chat_id
            )
            
            # Send response
            await update.message.reply_text(
                response, 
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            
        except Exception as e:
            logger.error(f"Error processing message from {user_id}: {e}")
            await update.message.reply_text(
                "🚧 Sorry, something went wrong. Please try again in a moment.",
                parse_mode='Markdown'
            )
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Sei MCP Bot...")
        self.app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    config = Config()
    config.validate()
    
    bot = SeiTelegramBot(config)
    bot.run()
```

### **Step 4: Deploy to Production**

**Option A: Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  sei-mcp-bot:
    build: .
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SEI_RPC_URL=${SEI_RPC_URL}
    ports:
      - "8000:8000"
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

**Option B: Railway Deployment**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Option C: Heroku Deployment**
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create sei-mcp-bot

# Set environment variables
heroku config:set TELEGRAM_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

### **Step 5: Environment Configuration**

**.env file:**
```bash
# Telegram Bot Configuration
TELEGRAM_TOKEN=your_telegram_bot_token_here

# AI Configuration  
OPENAI_API_KEY=your_openai_api_key_here

# Sei Network Configuration
SEI_RPC_URL=https://sei-evm-rpc.publicnode.com
SEI_REST_URL=https://sei-api.polkachu.com

# Optional: Custom endpoints
DEXSCREENER_API=https://api.dexscreener.com
SEITRACE_API=https://seitrace.com

# Bot Settings
MAX_RETRIES=3
REQUEST_TIMEOUT=30
CACHE_TTL=300
LOG_LEVEL=INFO
```

## 🔍 **Testing & Validation**

### **Test Commands**
```
# Wallet balance
0x742d35Cc6634C0532925a3b8D97B3cd

# Token analysis  
token 0x123...abc

# DeFi positions
portfolio

# NFT holdings
nft collections

# General questions
What's the best way to stake SEI?
```

## 📚 **Additional Resources**

### **Sei Network APIs**
- **RPC Endpoints**: [Sei RPC Documentation](https://docs.sei.io/dev-rpc)
- **REST APIs**: [Sei REST API](https://docs.sei.io/dev-rest)
- **Explorer APIs**: [SeiTrace API](https://seitrace.com/api)

### **MCP Resources**
- **MCP Specification**: [Model Context Protocol](https://modelcontextprotocol.io)
- **Tool Examples**: [MCP Tool Samples](https://github.com/modelcontextprotocol/tools)
- **Client Integration**: [Claude Desktop MCP](https://claude.ai/mcp)

### **Telegram Bot Resources**
- **Bot API**: [Telegram Bot API](https://core.telegram.org/bots/api)
- **Node.js Library**: [node-telegram-bot-api](https://github.com/yagop/node-telegram-bot-api)

## 🎯 **Next Steps**

1. **Fork/Clone** this repository as a starting point
2. **Set up MCP server** with basic Sei tools
3. **Create Telegram bot** and get API token
4. **Implement core features** one by one
5. **Test extensively** with real Sei addresses
6. **Deploy to production** and monitor usage
7. **Iterate and improve** based on user feedback

## 💡 **Pro Tips**

- **Start Simple**: Begin with wallet checking, then add complexity
- **Cache Data**: Implement caching for frequently requested data
- **Error Handling**: Graceful handling of network failures and invalid inputs
- **Rate Limiting**: Respect API limits and implement backoff strategies
- **Security**: Never log or store private keys or sensitive data
- **Monitoring**: Set up logging and alerts for production deployment

---

**Happy Building!** 🚀

This architecture gives you a solid foundation to create a powerful Telegram Sei MCP bot that can grow with your needs and the evolving Sei ecosystem.
