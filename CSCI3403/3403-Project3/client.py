"""
    client.py - Connect to an SSL server

    CSCI 3403
    Authors: Matt Niemiec and Abigail Fernandes
    Number of lines of code in solution: 117
        (Feel free to use more or less, this
        is provided as a sanity check)
    Put your team members' names: Parker Eischen



"""

import socket
from os import urandom
from random import choice
from string import ascii_uppercase
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from random import randint


iv = "G4XO4L\X<J;MPPLD"

host = "localhost"
port = 10001


# A helper function that you may find useful for AES encryption
def pad_message(message):
    return message + " "*((16-len(message))%16)


# TODO: Generate a random AES key
def generate_key():
    key =''.join(choice(ascii_uppercase) for i in range(16)) #creates key of byte length 16

    return key



# TODO: Takes an AES session key and encrypts it using the server's
# TODO: public key and returns the value
def encrypt_handshake(session_key,connection):
    serverString = connection.recv(1024)
    #print("publickey in handshake",serverString)
    serverPublicKey = RSA.importKey(serverString)
    #session_key = pad_message(session_key)
    encrypted = serverPublicKey.encrypt(bytes(session_key,'utf-8'),16)
    return encrypted[0]
    


# TODO: Encrypts the message using AES. Same as server function
def encrypt_message(message, session_key):
    # session_key = pad_message(session_key)
    aesKey = AES.new(session_key,AES.MODE_CBC,iv)
    message = pad_message(message)
    return aesKey.encrypt(message)


# TODO: Decrypts the message using AES. Same as server function
def decrypt_message(message, session_key):
    aesKey = AES.new(session_key,AES.MODE_CBC,iv)
    return aesKey.decrypt(message)


# Sends a message over TCP
def send_message(sock, message):
    sock.sendall(message)


# Receive a message from TCP
def receive_message(sock):
    data = sock.recv(1024)
    return data


def main():
    user = input("What's your username? ")
    password = input("What's your password? ")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Message that we need to send
        message = user + ' ' + password
        # TODO: Generate random AES key
        aesKey = generate_key()

        # TODO: Encrypt the session key using server's public key
        aesMessage = encrypt_handshake(aesKey,sock)
        send_message(sock,aesMessage)

        # Listen for okay from server (why is this necessary?)
        if receive_message(sock).decode() != "okay":
            print("Couldn't connect to server")
            exit(0)

        # TODO: Encrypt message and send to server
        encryptedMessage = encrypt_message(message,aesKey)
        send_message(sock,encryptedMessage)
        # TODO: Receive and decrypt response from server and print
        verificationEncripted = receive_message(sock)
        vericiation = decrypt_message(verificationEncripted,aesKey)
        print(vericiation.decode("utf-8"))
    finally:
        print('closing socket')
        sock.close()


if __name__ in "__main__":
    main()
