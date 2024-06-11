import os
import hashlib
from PIL import Image
from tqdm import tqdm


def calculate_image_hash(image_path):
    """Calcula o hash de uma imagem."""
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img = img.resize((256, 256))  # Redimensionar para normalizar o tamanho
        hash_md5 = hashlib.md5()
        for pixel in img.getdata():
            hash_md5.update(bytes(pixel))
        return hash_md5.hexdigest()

def find_duplicate_images(directory):
    """Encontra e remove imagens duplicadas em um diretório."""
    image_hashes = {}
    duplicates = []

    for root, _, files in os.walk(directory):
        for filename in tqdm(files):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                image_path = os.path.join(root, filename)
                image_hash = calculate_image_hash(image_path)

                if image_hash in image_hashes:
                    duplicates.append(image_path)
                else:
                    image_hashes[image_hash] = image_path

    return duplicates

def remove_duplicates(duplicates):
    """Remove os arquivos duplicados."""
    for duplicate in tqdm(duplicates):
        try:
            os.remove(duplicate)
            print(f"Removed duplicate image: {duplicate}")
        except Exception as e:
            print(f"Error removing file {duplicate}: {e}")

# Exemplo de uso:
directory = 'images'
duplicates = find_duplicate_images(directory)

if duplicates:
    print(f"Found {len(duplicates)} duplicate images.")
    remove_duplicates(duplicates)
else:
    print("No duplicate images found.")
