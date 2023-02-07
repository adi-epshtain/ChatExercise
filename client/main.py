from bl.chat_bl_v2 import ChatBLV2
import asyncio

async def main():
    chat_bl = ChatBLV2()
    await chat_bl.chat_client()

if __name__ == "__main__":
      asyncio.run(main())
    