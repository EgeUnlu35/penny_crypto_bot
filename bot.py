from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os
import re
import aiohttp
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get tokens from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Sei Network Configuration
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

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def classify_input(message: str):
    """Classify user input to determine appropriate tool"""
    patterns = {
        'wallet_sei': r'^(sei1[a-z0-9]{38})$',  # Sei native address
        'wallet_evm': r'^(0x[a-fA-F0-9]{40})$',  # EVM address
        'token': r'^(token|contract|price)\s+(0x[a-fA-F0-9]{40})$',
        'sei_price': r'^(sei\s+price|price\s+sei|\$sei|sei\s+chart)$',
        'defi': r'^(positions?|portfolio|defi|farming|staking)\s*(.*)?$',
        'nft': r'^(nft|nfts|collection)\s*(.*)?$',
        'help': r'^(help|commands?)$',
        'general': r'.*'  # Fallback
    }
    
    for input_type, regex in patterns.items():
        match = re.match(regex, message.strip(), re.IGNORECASE)
        if match:
            return {
                'type': input_type, 
                'data': match.group(1) if match.groups() else message,
                'full_match': match
            }
    
    return {'type': 'general', 'data': message, 'full_match': None}

async def check_sei_wallet(address: str, wallet_type: str = 'evm'):
    """Check Sei wallet balance and basic info"""
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            if wallet_type == 'evm':
                # Try multiple RPC endpoints
                rpc_endpoints = SEI_DATA_SOURCES['rpc']
                
                for rpc_url in rpc_endpoints:
                    try:
                        payload = {
                            "jsonrpc": "2.0",
                            "method": "eth_getBalance",
                            "params": [address, "latest"],
                            "id": 1
                        }
                        
                        async with session.post(
                            rpc_url,
                            json=payload,
                            headers={'Content-Type': 'application/json'}
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                if 'result' in data:
                                    balance_wei = int(data['result'], 16)
                                    balance_sei = balance_wei / (10**18)
                                    
                                    # Format response
                                    response_text = f"🔍 **Sei EVM Wallet Analysis**\n\n"
                                    response_text += f"📍 **Address**: `{address[:10]}...{address[-8:]}`\n"
                                    response_text += f"💰 **SEI Balance**: `{balance_sei:.6f} SEI`\n"
                                    response_text += f"🔗 **Explorer**: [View on SeiTrace]({SEI_DATA_SOURCES['explorer']}/address/{address})\n\n"
                                    
                                    if balance_sei > 0:
                                        response_text += f"✅ **Status**: Active wallet with funds\n"
                                    else:
                                        response_text += f"⚠️ **Status**: Empty wallet or new address\n"
                                    
                                    return response_text
                    except Exception as e:
                        print(f"RPC endpoint {rpc_url} failed: {e}")
                        continue
                
                return f"❌ All RPC endpoints failed. Sei network might be experiencing issues."
            
            elif wallet_type == 'sei':
                # Try multiple REST endpoints for native Sei addresses
                rest_endpoints = SEI_DATA_SOURCES['rest']
                
                for rest_url in rest_endpoints:
                    try:
                        async with session.get(
                            f"{rest_url}/cosmos/bank/v1beta1/balances/{address}",
                            headers={'Accept': 'application/json'}
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                balances = data.get('balances', [])
                                
                                response_text = f"🔍 **Sei Native Wallet Analysis**\n\n"
                                response_text += f"📍 **Address**: `{address[:10]}...{address[-8:]}`\n"
                                
                                sei_balance = 0
                                other_tokens = []
                                
                                if balances:
                                    for balance in balances:
                                        denom = balance['denom']
                                        amount = int(balance['amount'])
                                        
                                        if denom == 'usei':
                                            sei_balance = amount / (10**6)  # usei to SEI
                                        else:
                                            other_tokens.append(f"🪙 **{denom}**: `{amount}`")
                                
                                response_text += f"💰 **SEI Balance**: `{sei_balance:.6f} SEI`\n"
                                
                                # Add other tokens if any
                                if other_tokens:
                                    response_text += f"\n**Other Tokens:**\n"
                                    for token in other_tokens[:5]:  # Limit to 5 tokens
                                        response_text += f"{token}\n"
                                
                                response_text += f"\n🔗 **Explorer**: [View on SeiTrace]({SEI_DATA_SOURCES['explorer']}/account/{address})\n"
                                
                                if sei_balance > 0:
                                    response_text += f"✅ **Status**: Active wallet with funds"
                                else:
                                    response_text += f"⚠️ **Status**: Empty wallet or new address"
                                
                                return response_text
                                
                    except Exception as e:
                        print(f"REST endpoint {rest_url} failed: {e}")
                        continue
                
                # If all REST endpoints fail, try alternative approach
                return await check_sei_wallet_fallback(address)
                        
    except Exception as e:
        return f"❌ Error analyzing wallet: {str(e)}"

async def check_sei_wallet_fallback(address: str):
    """Fallback method using alternative APIs"""
    try:
        # Try using a blockchain explorer API as fallback
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            # Alternative: Try mintscan API
            try:
                async with session.get(
                    f"https://lcd-sei.cosmostation.io/cosmos/bank/v1beta1/balances/{address}"
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        balances = data.get('balances', [])
                        
                        response_text = f"🔍 **Sei Native Wallet Analysis** *(via fallback)*\n\n"
                        response_text += f"📍 **Address**: `{address[:10]}...{address[-8:]}`\n"
                        
                        sei_balance = 0
                        if balances:
                            for balance in balances:
                                if balance['denom'] == 'usei':
                                    sei_balance = int(balance['amount']) / (10**6)
                                    break
                        
                        response_text += f"💰 **SEI Balance**: `{sei_balance:.6f} SEI`\n"
                        response_text += f"🔗 **Explorer**: [View on SeiTrace]({SEI_DATA_SOURCES['explorer']}/account/{address})\n\n"
                        response_text += f"⚠️ **Note**: Retrieved via fallback API due to network issues"
                        
                        return response_text
            except:
                pass
                
        # If everything fails, return a helpful error message
        return f"""❌ **Unable to fetch wallet data**

The Sei network APIs are currently experiencing issues. Please try again in a few minutes.

🔗 **Manual Check**: You can view this wallet directly at:
[{SEI_DATA_SOURCES['explorer']}/account/{address}]({SEI_DATA_SOURCES['explorer']}/account/{address})

**Address**: `{address}`"""
        
    except Exception as e:
        return f"❌ Error in fallback method: {str(e)}"

async def analyze_sei_token(contract_address: str):
    """Analyze token data from DexScreener API"""
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            # Try DexScreener API for Sei tokens
            url = f"{SEI_DATA_SOURCES['dex']}/latest/dex/tokens/{contract_address}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('pairs') and len(data['pairs']) > 0:
                        # Get the most liquid pair (first one is usually best)
                        pair = data['pairs'][0]
                        
                        response_text = f"📊 **Token Analysis**\n\n"
                        response_text += f"📍 **Contract**: `{contract_address[:10]}...{contract_address[-8:]}`\n"
                        response_text += f"🏷️ **Name**: {pair.get('baseToken', {}).get('name', 'Unknown')}\n"
                        response_text += f"🔤 **Symbol**: {pair.get('baseToken', {}).get('symbol', 'Unknown')}\n\n"
                        
                        # Price information
                        price_usd = pair.get('priceUsd')
                        if price_usd:
                            response_text += f"💰 **Price**: ${float(price_usd):.8f}\n"
                        
                        # Volume information
                        volume_24h = pair.get('volume', {}).get('h24')
                        if volume_24h:
                            response_text += f"📈 **24h Volume**: ${float(volume_24h):,.2f}\n"
                        
                        # Market cap
                        market_cap = pair.get('marketCap')
                        if market_cap:
                            response_text += f"🏪 **Market Cap**: ${float(market_cap):,.2f}\n"
                        
                        # Price changes
                        price_change_24h = pair.get('priceChange', {}).get('h24')
                        if price_change_24h:
                            change_float = float(price_change_24h)
                            emoji = "🟢" if change_float >= 0 else "🔴"
                            response_text += f"{emoji} **24h Change**: {change_float:.2f}%\n"
                        
                        # Liquidity
                        liquidity = pair.get('liquidity', {}).get('usd')
                        if liquidity:
                            response_text += f"💧 **Liquidity**: ${float(liquidity):,.2f}\n"
                        
                        # DEX information
                        dex_id = pair.get('dexId', 'Unknown')
                        response_text += f"🏦 **DEX**: {dex_id.title()}\n"
                        
                        # Links
                        response_text += f"\n🔗 **Links**:\n"
                        response_text += f"• [DexScreener]({pair.get('url', '#')})\n"
                        response_text += f"• [SeiTrace]({SEI_DATA_SOURCES['explorer']}/token/{contract_address})\n"
                        
                        # Risk warning for new/low liquidity tokens
                        if liquidity and float(liquidity) < 10000:
                            response_text += f"\n⚠️ **Warning**: Low liquidity token - trade with caution!"
                        
                        return response_text
                    else:
                        return f"❌ **Token not found**\n\nNo trading pairs found for this contract address. The token might be:\n• Not yet listed on DEXs\n• Invalid contract address\n• Not deployed on Sei Network"
                else:
                    return f"❌ **API Error**: Unable to fetch token data (Status: {response.status})"
                    
    except Exception as e:
        return f"❌ **Error analyzing token**: {str(e)}"

async def get_sei_price():
    """Get current SEI token price"""
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            # Try to get SEI price from DexScreener
            url = f"{SEI_DATA_SOURCES['dex']}/latest/dex/search?q=SEI"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Find SEI/USDC or SEI/USDT pair
                    sei_pairs = []
                    if data.get('pairs'):
                        for pair in data['pairs']:
                            base_symbol = pair.get('baseToken', {}).get('symbol', '').upper()
                            quote_symbol = pair.get('quoteToken', {}).get('symbol', '').upper()
                            
                            if base_symbol == 'SEI' and quote_symbol in ['USDC', 'USDT']:
                                sei_pairs.append(pair)
                    
                    if sei_pairs:
                        # Use the pair with highest liquidity
                        best_pair = max(sei_pairs, key=lambda x: float(x.get('liquidity', {}).get('usd', 0)))
                        
                        response_text = f"💰 **SEI Price Analysis**\n\n"
                        
                        price_usd = best_pair.get('priceUsd')
                        if price_usd:
                            response_text += f"💵 **Current Price**: ${float(price_usd):.4f}\n"
                        
                        # Price changes
                        price_change_24h = best_pair.get('priceChange', {}).get('h24')
                        if price_change_24h:
                            change_float = float(price_change_24h)
                            emoji = "🟢" if change_float >= 0 else "🔴"
                            response_text += f"{emoji} **24h Change**: {change_float:.2f}%\n"
                        
                        # Volume
                        volume_24h = best_pair.get('volume', {}).get('h24')
                        if volume_24h:
                            response_text += f"📊 **24h Volume**: ${float(volume_24h):,.2f}\n"
                        
                        # Market cap
                        market_cap = best_pair.get('marketCap')
                        if market_cap:
                            response_text += f"🏪 **Market Cap**: ${float(market_cap):,.2f}\n"
                        
                        response_text += f"\n🏦 **Trading on**: {best_pair.get('dexId', 'Unknown').title()}"
                        response_text += f"\n🔗 [View Chart]({best_pair.get('url', '#')})"
                        
                        return response_text
                    else:
                        return f"❌ **SEI price data not found**\n\nUnable to find SEI trading pairs on supported DEXs."
                else:
                    return f"❌ **API Error**: Unable to fetch SEI price (Status: {response.status})"
                    
    except Exception as e:
        return f"❌ **Error fetching SEI price**: {str(e)}"

async def get_help_message():
    """Generate help message with available commands"""
    help_text = """
🤖 **Penny Crypto Bot - Sei Network Assistant**

**💰 Wallet Analysis:**
• Send any Sei wallet address to get balance info
• Supports both EVM (0x...) and Native (sei1...) addresses
• Example: `0x1234...` or `sei1abc...`

**� Token Analysis:**
• `token 0x1234...` - Analyze any Sei token
• `sei price` - Get current SEI price
• `price sei` - SEI price and market data
• `$sei` - Quick SEI price check

**🔮 Coming Soon:**
• DeFi portfolio management  
• NFT collection explorer
• Price alerts and notifications
• Cross-chain analysis

**💬 General AI Chat:**
• Ask me anything about crypto, Sei Network, or DeFi
• I'm powered by ChatGPT with Sei expertise!

**📚 Commands:**
• `/start` - Welcome message
• `/help` - Show this help
• Just send a wallet address or token contract for instant analysis!

Built with ❤️ for the Sei community
    """
    return help_text.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🤖 **Welcome to Penny Crypto Bot!**

Your AI-powered assistant for the Sei Network ecosystem!

🔍 **Try these features:**
• Send any Sei wallet address for instant analysis
• Analyze tokens with contract addresses
• Get real-time SEI price data
• Ask questions about Sei, DeFi, or crypto
• Get help with `/help`

**Examples:**
• `sei1abc123...` (Native Sei address)
• `0x1234abcd...` (EVM address or token contract)
• `token 0x1234...` (Token analysis)
• `sei price` (SEI price check)
• `"What is Sei Network?"` (AI chat)
• `"How does Astroport work?"` (DeFi questions)

Ready to explore Sei? Send me a wallet address or try `sei price`! 🚀
    """
    await update.message.reply_text(welcome_text.strip(), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    classification = classify_input(user_message)
    
    try:
        # Send "typing..." indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Handle different input types
        if classification['type'] == 'wallet_evm':
            # EVM address analysis
            response_text = await check_sei_wallet(classification['data'], 'evm')
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
        elif classification['type'] == 'wallet_sei':
            # Native Sei address analysis
            response_text = await check_sei_wallet(classification['data'], 'sei')
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
        elif classification['type'] == 'token':
            # Token analysis - extract contract address from the match
            contract_address = classification['full_match'].group(2)
            response_text = await analyze_sei_token(contract_address)
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
        elif classification['type'] == 'sei_price':
            # SEI price analysis
            response_text = await get_sei_price()
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
        elif classification['type'] == 'help':
            # Help command
            help_text = await get_help_message()
            await update.message.reply_text(help_text, parse_mode='Markdown')
            
        elif classification['type'] in ['defi', 'nft']:
            # Future features placeholder
            feature_name = classification['type'].upper()
            response_text = f"🚧 **{feature_name} Analysis Coming Soon!**\n\n"
            response_text += f"I'm working on adding {feature_name.lower()} analysis features.\n"
            response_text += "For now, try:\n• Wallet analysis (send address)\n• Token analysis (`token 0x123...`)\n• SEI price (`sei price`)\n• Ask me anything about crypto!"
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
        else:
            # Fallback to ChatGPT with Sei context
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a helpful assistant specializing in the Sei Network blockchain and cryptocurrency. 

Key information about Sei:
- Sei is a Layer 1 blockchain optimized for trading and DeFi
- It features both EVM and CosmWasm support
- Major protocols include Astroport, Kryptic, Levana, White Whale
- Native token is SEI
- Supports both native (sei1...) and EVM (0x...) addresses

Provide accurate, helpful information about Sei Network, DeFi protocols, cryptocurrency trading, and blockchain technology. If you're unsure about specific details, acknowledge the limitation."""},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            await update.message.reply_text(ai_response)
        
    except Exception as e:
        error_text = f"❌ **Error**: {str(e)}\n\n"
        error_text += "Try again or send `/help` for available commands."
        await update.message.reply_text(error_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = await get_help_message()
    await update.message.reply_text(help_text, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
