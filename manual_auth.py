import asyncio
import aiohttp
import os
from aiohttp import ClientSession
from xbox.webapi.authentication.manager import AuthenticationManager
from dotenv import load_dotenv
load_dotenv()
async def authenticate():
    async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        auth_mgr = AuthenticationManager(
            session, 
            client_id=os.getenv("XBL_CID", ""),
            client_secret=os.getenv("XBL_CSEC", ""),
            redirect_uri=""
        )
        print("Starting authentication...")
        auth_url = auth_mgr.generate_authorization_url()
        print(f"\nPlease visit this URL to authenticate:\n{auth_url}\n")
        redirect_url = input("After logging in, paste the full URL you were redirected to: ")
        await auth_mgr.request_tokens(redirect_url)
        tokens_path = os.getenv("XBL_TOKENS_PATH", 
                                os.path.expanduser("~/.local/openxbox/tokens.json"))
        os.makedirs(os.path.dirname(tokens_path), exist_ok=True)
        with open(tokens_path, "w") as f:
            f.write(auth_mgr.oauth.json())
        print(f"\nTokens saved to {tokens_path}")
        print(f"Logged in as: {auth_mgr.xsts_token.gamertag}")
if __name__ == "__main__":
    asyncio.run(authenticate())
