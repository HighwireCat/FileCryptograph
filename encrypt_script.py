from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


def encrypt_file(file_path, key, output_file):
    # Read the file
    with open(file_path, 'rb') as f:
        data = f.read()

    # Pad the data
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Generate a random IV
    iv = os.urandom(16)

    # Create cipher object and encrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Write the IV and encrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)


# File paths
input_file_path = 'Test_files/document.pdf'
encrypted_file_path = 'Encrypted_Files/Encrypted_document.pdf'

# Generate a random 256-bit key
key = os.urandom(32)

# Encrypt the file
encrypt_file(input_file_path, key, encrypted_file_path)
