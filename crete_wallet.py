# pip install eth-account python-dotenv
from pathlib import Path

from dotenv import set_key
from eth_account import Account

ENV_PATH = Path(__file__).parent / ".env"

acct = Account.create()
ENV_PATH.touch(exist_ok=True)
set_key(ENV_PATH, "PRIVATE_KEY", "0x" + acct.key.hex())
set_key(ENV_PATH, "WALLET_ADDRESS", acct.address)

print("Address:", acct.address)  # share this with faucets
print(f"Private key saved to {ENV_PATH}")  # keep this secret
