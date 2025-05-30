download_mirror = "https://us.openslr.org/resources/12/dev-clean.tar.gz"

import os
import tarfile
import requests
from tqdm import tqdm

def download_file(url, save_path):
    """
    Download a file from a URL with progress bar
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Check if file already exists
    if os.path.exists(save_path):
        print(f"File already exists at {save_path}")
        return save_path
    
    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    # Get file size for progress bar
    total_size = int(response.headers.get('content-length', 0))
    
    # Download with progress bar
    with open(save_path, 'wb') as file, tqdm(
        desc=os.path.basename(save_path),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = file.write(chunk)
            bar.update(size)
    
    return save_path

def extract_tarfile(tar_path, extract_path):
    """
    Extract a tar.gz file
    """
    os.makedirs(extract_path, exist_ok=True)
    
    with tarfile.open(tar_path) as tar:
        members = tar.getmembers()
        for member in tqdm(members, desc="Extracting"):
            tar.extract(member, path=extract_path)
    
    return extract_path

# Download LibriSpeech dev-clean dataset
data_dir = "data"
tar_path = os.path.join(data_dir, "dev-clean.tar.gz")
extract_path = os.path.join(data_dir, "librispeech")

print(f"Downloading LibriSpeech dev-clean from {download_mirror}...")
download_file(download_mirror, tar_path)

print(f"Extracting to {extract_path}...")
extract_tarfile(tar_path, extract_path)

print("Download and extraction complete!")
