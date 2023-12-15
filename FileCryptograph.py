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


def decrypt_file(file_path, key, output_file):
    # Read the IV and encrypted data
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()

    # Create cipher object and decrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the data
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(data)


# File paths
input_file_path = 'Test_files/document.pdf'
encrypted_file_path = 'Encrypted_Files/Encrypted_document.pdf'
decrypted_file_path = 'Decrypted_Files/Decrypted_document.pdf'

# Generate a random 256-bit key
key = os.urandom(32)

# Encrypt the file
encrypt_file(input_file_path, key, encrypted_file_path)

# Decrypt the file (for testing purposes)
decrypt_file(encrypted_file_path, key, decrypted_file_path)
