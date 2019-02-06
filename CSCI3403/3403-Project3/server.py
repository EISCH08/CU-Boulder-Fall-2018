"""
    server.py - host an SSL server that checks passwords

    CSCI 3403
    Authors: Matt Niemiec and Abigail Fernandes
    Number of lines of code in solution: 140
        (Feel free to use more or less, this
        is provided as a sanity check)

    Put your team members' names: Parker Eischen



"""

import socket
from os import chmod
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
import hashlib
import uuid



iv = "G4XO4L\X<J;MPPLD"

host = "localhost"
port = 10001

def generateRSA(bits = 1024):
    random = Random.new().read
    privateKey = RSA.generate(bits,random)
    publicKey = privateKey.publickey()
    return publicKey,privateKey

publicKey,privateKey = generateRSA(1024)
# A helper function. It may come in handy when performing symmetric encryption
def pad_message(message):
    return message + " " * ((16 - len(message)) % 16)


# TODO: Write a function that decrypts a message using the server's private key
def decrypt_key(session_key):
    decrypted = privateKey.decrypt(session_key)
    return(decrypted)


# TODO: Write a function that decrypts a message using the session key
def decrypt_message(client_message, session_key):
    aesKey = AES.new(session_key,AES.MODE_CBC,iv)

    return aesKey.decrypt(client_message)


# TODO: Encrypt a message using the session key
def encrypt_message(message, session_key):
    aesKey = AES.new(session_key,AES.MODE_CBC,iv)
    message = pad_message(message)
    return aesKey.encrypt(message)


# Receive 1024 bytes from the client
def receive_message(connection):
    return connection.recv(1024)


# Sends message to client
def send_message(connection, data):
    if not data:
        print("Can't send empty string")
        return
    if type(data) != bytes:
        data = data.encode()
    connection.sendall(data)


# A function that reads in the password file, salts and hashes the password, and
# checks the stored hash of the password to see if they are equal. It returns
# True if they are and False if they aren't
def verify_hash(user, password):
    try:
        reader = open("passfile.txt", 'r')
        for line in reader.read().split('\n'):
            line = line.split("\t")
            #print(line[0],user)
            if line[0] == user:
                hashed_password = hashlib.sha512((password + line[1]).encode()).hexdigest()
                if(line[2] == hashed_password):
                    return True
        reader.close()
    except FileNotFoundError:
        return False
    return False


def main():
    # Set up network connection listener
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (host, port)
    print('starting up on {} port {}'.format(*server_address))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(server_address)
    sock.listen(1)

    try:
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                print('connection from', client_address)

                send_message(connection,publicKey.exportKey())
                #print("PublicKey Sent to Client")
                # Receive encrypted key from client
                encrypted_key = receive_message(connection)
                #print("Received encrypted_key")
                # Send okay back to client
                send_message(connection, "okay")

                # Decrypt key from client
                #print(type(encrypted_key))
                plaintext_key = decrypt_key(encrypted_key)
                #print(plaintext_key)

                # Receive encrypted message from client
                ciphertext_message = receive_message(connection)
                #print("Received ciphertext_message:",ciphertext_message)
                # Decrypt message from client
                plaintext_message = decrypt_message(ciphertext_message, plaintext_key)

                # Split response from user into the username and password
                user, password = plaintext_message.split()

                if verify_hash(user.decode("utf-8"), password.decode("utf-8")):
                    plaintext_response = "User successfully authenticated!"
                else:
                    plaintext_response = "Password or username incorrect"

                # Encrypt response to client
                plaintext_key = plaintext_key.decode("utf-8")
                ciphertext_response = encrypt_message(plaintext_response, plaintext_key)
                
                # Send encrypted response
                send_message(connection, ciphertext_response)
            finally:
                # Clean up the connection
                connection.close()
    finally:
        sock.close()


if __name__ in "__main__":
    main()
