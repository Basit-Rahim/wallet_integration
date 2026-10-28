"""Read ETH and USDC balances on Ethereum Sepolia."""
import os
from decimal import Decimal

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Free public RPC. You can swap in your own (Alchemy/Infura/QuickNode) via .env later.
RPC_URL = os.getenv("SEPOLIA_RPC_URL", "https://ethereum-sepolia-rpc.publicnode.com")
SEPOLIA_CHAIN_ID = 11155111

MY_ADDRESS = Web3.to_checksum_address("0x2264BD2FBfdba6177319c0525E6ca643f64827E6")
USDC_ADDRESS = Web3.to_checksum_address("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238")

# Minimal ABI: only the functions we call.
ERC20_ABI = [
    {"name": "balanceOf", "type": "function", "stateMutability": "view",
     "inputs": [{"name": "owner", "type": "address"}],
     "outputs": [{"name": "", "type": "uint256"}]},
    {"name": "decimals", "type": "function", "stateMutability": "view",
     "inputs": [], "outputs": [{"name": "", "type": "uint8"}]},
    {"name": "symbol", "type": "function", "stateMutability": "view",
     "inputs": [], "outputs": [{"name": "", "type": "string"}]},
]


def main():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    # Safety checks: are we connected, and to the RIGHT network?
    if not w3.is_connected():
        raise SystemExit(f"Cannot connect to RPC: {RPC_URL}")
    if w3.eth.chain_id != SEPOLIA_CHAIN_ID:
        raise SystemExit(f"Wrong network! chain_id={w3.eth.chain_id}")

    # 1) Native ETH balance (returned in wei, 18 decimals)
    wei = w3.eth.get_balance(MY_ADDRESS)
    eth = Web3.from_wei(wei, "ether")
    print(f"ETH : {eth} (raw wei: {wei})")

    # 2) USDC balance (ERC-20 token, call the contract)
    usdc = w3.eth.contract(address=USDC_ADDRESS, abi=ERC20_ABI)
    raw = usdc.functions.balanceOf(MY_ADDRESS).call()
    decimals = usdc.functions.decimals().call()
    symbol = usdc.functions.symbol().call()
    amount = Decimal(raw) / Decimal(10**decimals)
    print(f"{symbol}: {amount} (raw units: {raw}, decimals: {decimals})")


if __name__ == "__main__":
    main()