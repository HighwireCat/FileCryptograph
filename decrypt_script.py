from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


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
encrypted_file_path = 'Encrypted_Files/Encrypted_document.pdf'
decrypted_file_path = 'Decrypted_Files/Decrypted_document.pdf'

# Key used for decryption (must be the same as used for encryption)
key = b'YourKeyHere'  # Replace with the actual key

# Decrypt the file
decrypt_file(encrypted_file_path, key, decrypted_file_path)
