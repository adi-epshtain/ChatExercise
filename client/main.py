from bl.chat_bl_v2 import chat_client
import asyncio

async def main():
    await chat_client()

if __name__ == "__main__":
      asyncio.run(main())
    