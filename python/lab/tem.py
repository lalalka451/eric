import aiohttp
import ssl
from pathlib import Path
import hashlib
import logging
import asyncio


def get_md5(raw: bytes) -> str:
    md5_hash = hashlib.md5()
    md5_hash.update(raw)
    return md5_hash.hexdigest().upper()

async def download_picture(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        ssl_context = None
        if "multimedia.nt.qq.com.cn" in url:
            ssl_context = ssl.create_default_context()
            ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
            ssl_context.set_ciphers("HIGH:!aNULL:!MD5")
        async with session.get(url, ssl=ssl_context) as resp:
            return await resp.read()

async def try_download_image(url: str, base_path: Path):
    raw = await download_picture(url)
    img_type = "jpg"  # Assuming the image type is jpg for this example
    if img_type != "Unknown":
        save_path = base_path / f"{get_md5(raw)}.{img_type.lower()}"
        save_path.write_bytes(raw)
        print(f"图片已缓存至{save_path.as_posix()}")
    else:
        save_path = base_path / f"{get_md5(raw)}.png"
        save_path.write_bytes(raw)
        print(f"未知类型图片！尝试保存为PNG格式")

url = 'https://multimedia.nt.qq.com.cn/download?appid=1407&amp;fileid=EhT3_Fl_iBiQb7BZDgxo4dFaT2riPRigUCD_Cii506muhbOJAzIEcHJvZFCAvaMBWhC25FHoY7UE5Dwcai6zStrR&amp;spec=0&amp;rkey=CAMSKMa3OFokB_TlDJZKuCF8ehYKB3e1uR-JLkPeetXj7P1XNr7kL6zrXRM,file_size=10272,file_unique=C3D92A0B16FC24F039FAD9ED1BF41B89.jpg'
base_path = Path(r"C:\Users\fueqq\Downloads\tem")

# Add this block to run the coroutine
async def main():
    await try_download_image(url, base_path)

# Run the event loop
asyncio.run(main())
