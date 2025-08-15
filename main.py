import os
import requests
import random
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
API_TOKEN = os.environ.get('6043450746:AAG5WoXNn3TBqacMLvQIdCCuoJBQDQ6uE9Q')
APP_NAME = "Fox_Fast_Bot"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def random_host() -> str:
    try:
        r = requests.get("https://api.audius.co", timeout=5)
        hosts = r.json().get("data", [])
        if hosts:
            return random.choice(hosts)
    except Exception:
        pass
    return"https://discoveryprovider.audius.co"

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer("Menga qoshiqni nomini jonating men sizga qoshiqni topib beraman🔍")

@dp.message(F.text)
async def search(m: Message):
    query = (m.text or "").strip()
    limit = 5
    if not query or query.startswith('/'):
            return
    await m.answer("Qoshiqni istayapmiz🔍")

    host = random_host()

    try:
        resp = requests.get(f"{host}/v1/tracks/search",
        params={"query": query,"app_name": APP_NAME, "limit": limit}, timeout=10)
        data = resp.json().get("data", [])
    except Exception as e:
        await m.answer("Server qoshiq topilmadi❌")
        return
    if not data:
        await m.answer("Server qoshiq topilmadi❌")
        return
    for track in data:
        track_id = track["id"]
        title = track.get("title", "Unknown")
        artist =track.get("user", {}).get("name", "Unknown")
        stream_url = f"{host}/v1/tracks/{track_id}/stream?app_name={APP_NAME}"

        try:
            await m.answer_audio(
                audio= stream_url,
                title = title,
                performer = artist,
                caption = f"{title} - {artist}"
            )
        except Exception:
            permalink = track.get("permalink", "")
            link = f"https://audius.co{permalink}" if permalink else stream_url
            await m.answer(f"Audio ni topo olmadik mana havola:\n{link}")

async def main():
    print('Bot started🚀')
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
