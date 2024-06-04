import os
import requests
from cryptography.fernet import Fernet
import getpass
import json

# Function to generate and save the encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Function to prompt the user for credentials and save them encrypted
def save_encrypted_credentials():
    # Generate and save the key if it doesn't exist
    if not os.path.exists("secret.key"):
        generate_key()

    key = load_key()
    cipher_suite = Fernet(key)

    # Prompt the user for a username and password
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Encrypt the credentials
    encrypted_username = cipher_suite.encrypt(username.encode())
    encrypted_password = cipher_suite.encrypt(password.encode())

    # Save the encrypted credentials to a file
    with open("encrypted_credentials.bin", "wb") as credentials_file:
        credentials_file.write(encrypted_username + b'\n' + encrypted_password)

    print("Credentials encrypted and saved successfully.")

# Function to load and decrypt the credentials
def load_decrypted_credentials():
    key = load_key()
    cipher_suite = Fernet(key)

    # Load the encrypted credentials
    with open("encrypted_credentials.bin", "rb") as credentials_file:
        encrypted_username, encrypted_password = credentials_file.read().split(b'\n')

    # Decrypt the credentials
    username = cipher_suite.decrypt(encrypted_username).decode()
    password = cipher_suite.decrypt(encrypted_password).decode()

    return username, password

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

vault_domain = config["api_info"]["vault_domain"]
api_version = config["api_info"]["api_version"]
auth_endpoint = f"{vault_domain}/api/{api_version}/auth"

# Function to authenticate and get session ID
def authenticate():
    username, password = load_decrypted_credentials()
    response = requests.post(auth_endpoint, data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["sessionId"]
    else:
        raise Exception("Authentication failed")