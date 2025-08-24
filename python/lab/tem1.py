import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import sys

def fetch_image(url):
    """
    Fetches image data from the specified URL.

    Args:
        url (str): The URL of the encrypted image.

    Returns:
        bytes: The binary content of the image.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Successfully fetched image from {url}")
        return response.content
    except Exception as e:
        print(f"Error fetching image from {url}: {e}")
        sys.exit(1)

def decrypt_image(encrypted_base64, key, iv):
    """
    Decrypts encrypted base64 bytes using AES-CBC.

    Args:
        encrypted_base64 (str): The encrypted base64 string.
        key (bytes): The AES key (must be 16, 24, or 32 bytes long).
        iv (bytes): The Initialization Vector (must be 16 bytes long).

    Returns:
        bytes: The decrypted binary data.
    """
    try:
        # Decode base64 encoded data
        encrypted_bytes = base64.b64decode(encrypted_base64)

        # Initialize AES cipher in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt and remove padding
        decrypted_padded = cipher.decrypt(encrypted_bytes)
        decrypted = unpad(decrypted_padded, AES.block_size)

        print("Decryption successful.")
        return decrypted
    except (ValueError, KeyError) as e:
        print(f"Error during decryption: {e}")
        sys.exit(1)

def save_image(decrypted_bytes, output_path):
    """
    Saves decrypted binary image data to a file.

    Args:
        decrypted_bytes (bytes): The decrypted image data.
        output_path (str): The file path to save the decrypted image.
    """
    try:
        with open(output_path, 'wb') as f:
            f.write(decrypted_bytes)
        print(f"Decrypted image saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

def main():
    """
    Main function to orchestrate fetching, decrypting, and saving the image.
    """
    # Replace with your encrypted image URL and desired output path
    image_url = "https://pic.shyzckj.cn/upload_01/position/20241005/2024100500501626680.jpg"
    output_path = "/media/decrypted_image.jpg"  # Changed to relative path for broader compatibility

    # Step 1: Fetch the encrypted image
    encrypted_data = fetch_image(image_url)

    # Step 2: Define AES key and IV
    key_str = 'enc'
    iv_str = 'iv12'

    # Pad key and IV with null bytes to meet AES requirements (16 bytes for AES-128)
    key = key_str.encode('utf-8').ljust(16, b'\x00')  # b'enc\x00\x00...'
    iv = iv_str.encode('utf-8').ljust(16, b'\x00')    # b'iv12\x00\x00...'

    print(f"Using AES Key: {key}")
    print(f"Using AES IV: {iv}")

    # Step 3: Decode the encrypted image base64 string
    encrypted_base64 = encrypted_data.decode('utf-8')

    # Step 4: Decrypt the bytes directly
    decrypted_bytes = decrypt_image(encrypted_base64, key, iv)

    # Step 5: Save the decrypted image to file
    save_image(decrypted_bytes, output_path)

if __name__ == "__main__":
    main()