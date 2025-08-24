import requests
import os
from PIL import Image
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def download_image(url, save_path, format='GIF'):
    headers = {
        "Sec-Ch-Ua-Platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "image",
        "Referer": "https://www.douyin.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "i"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        img = Image.open(io.BytesIO(response.content))

        # Ensure the desired format is supported
        if format.upper() not in Image.registered_extensions().values():
            logging.warning(f"Format {format} is not recognized. Saving in original format {img.format}.")
            format = img.format if img.format else 'PNG'

        img.save(save_path, format.upper())

        logging.info(f"Image downloaded successfully and saved as {format.upper()} to {save_path}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image. Error: {e}")
    except IOError as e:
        logging.error(f"Failed to process/save image. Error: {e}")


# URL of the image to download
image_url = "https://p3-sign.douyinpic.com/obj/douyin-user-image-file/be6f3bccfba2c0932a566490e737dd0f?x-expires=1728212400&x-signature=azEwcahhp%2B0tBtzCILpHf9%2F5Ot8%3D&from=2064092626&s=sticker_comment&se=false&sc=sticker_heif&biz_tag=aweme_comment&l=2024100613242617A5BA66C4063429F077"

# Path where the image will be saved
save_path = "downloaded_images/sticker.gif"

# Download the image
download_image(image_url, save_path, format='GIF')