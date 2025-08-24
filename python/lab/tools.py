import requests
import os


def download_image(url, headers=None, filename="downloaded_image.png"):
    """
    Download an image from the given URL.

    :param url: URL of the image to download
    :param headers: Optional headers for the request
    :param filename: Name to save the file as (default: "downloaded_image.png")
    :return: Path of the saved image or None if download failed
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Create the full path for saving the image
        image_path = os.path.join(script_dir, filename)

        # Save the image
        with open(image_path, 'wb') as file:
            file.write(response.content)
        os.remove(image_path)
        print(f"Image downloaded successfully and saved as {image_path}")
        return image_path

    except requests.RequestException as e:
        print(f"Failed to download image: {e}")
        return None

