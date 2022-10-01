# Import Python modules

# Python socket module for handling web sockets
from socket import socket, AF_INET, SOCK_STREAM

# Python os module for handling file paths
import os

# Python mimetypes module for handling mime types
import mimetypes


# IP address of localhost
LOCALHOST = "127.0.0.1"

# Port number to listen on
PORT = 2728


# Function to extract method, path, parameters from the client request
def extract(header):
    # Header is split the into lines and then into words
    request_header = header.split("\r\n")
    request = request_header[0].split(" ")
    # First word is the method
    method = request[0]
    # Second word is the url
    url = request[1]

    # Split the url into path and parameters
    path_parameters = url.split("?")
    # The first part is the path
    path = path_parameters[0]

    # creating a dictionary for the parameters
    parames = path_parameters[1] if len(path_parameters) > 1 else ""
    parames = parames.split("&") if len(parames) > 0 else []
    paramsObject = {}
    if parames:
        paramsObject = {param.split("=")[0]: param.split("=")[
            1] for param in parames}

    # return the method, path, and parameters
    return method, path, paramsObject


# Function to resolve the path of a file corresponding to request path
def resol_path(path):
    # When the path is empty, set it to index.html
    if path == "/":
        return os.path.join(os.getcwd(), "htdocs", "index.html")

    # Dividing the path into segments and remove first empty segment
    segments = path.split("/")
    # Delete first segment
    segments.pop(0)

    # When last segment is empty, simply drop it
    if segments[-1] == "":
        segments.pop(-1)

    # add .html extension to the end of the path to get the file name
    if "." not in segments[-1]:
        segments[-1] = segments[-1] + ".html"

    # join the segments and get the absolute file path
    return os.path.join(os.getcwd(), "htdocs", *segments)


# Function for genarate the response header
def resp(status=200, content="", content_type="text/html"):

    # checking if the type is image or not
    if "image" in content_type:
        # if image, set Accept Range to bytes and drop content length
        cont_length = ""
        acc_ranges = "Accept-Ranges: bytes\r\n"
    else:
        # if not image, set content length and remove Accept Range
        cont_length = f"Content-Length: {len(content)}\r\n"
        acc_ranges = ""

    # successfull responces
    if 200 <= status < 300:
        return f'HTTP/1.1 {status} OK\r\n{cont_length}content-type: {content_type}\r\n{acc_ranges}\r\n'

    # client error responces
    if 400 <= status < 500:
        return f"HTTP/1.1 {status} Not Found\r\nContent-Length: {len(content)}\r\n\r\n"

    # server error responces
    if 500 <= status < 600:
        return f"HTTP/1.1 {status} Server Error\r\nContent-Length: {len(content)}\r\n\r\n"


# Handling the request
with socket(AF_INET, SOCK_STREAM) as server:

    # Binding the server to the localhost and port
    server.bind((LOCALHOST, PORT))

    # Listening for connections
    server.listen()
    print("Listening on port", PORT)

    while True:
        # Accepting the client request
        client, _ = server.accept()

        recv_header = client.recv(1024).decode()

        try:
            method, path, _ = extract(recv_header)

            # Handling GET Method
            if method == 'GET':
                try:
                    f_path = resol_path(path)
                    print("sent: ", f_path)
                    f_type = mimetypes.guess_type(f_path)[0]

                    # Checking if the file is a image or not
                    if "image" in f_type:

                        # Opening file as read bytes mode
                        with open(f_path, 'rb') as f:
                            file = f.read()
                            # Sending the response header
                            client.send(
                                resp(status=200, content_type=f_type).encode())
                            # Sending the file
                            client.send(file)
                    else:
                        # Getting the content of the file
                        with open(f_path, "r") as f:
                            content = f.read()

                        # Sending the response header
                        client.send(resp(status=200, content=content,
                                    content_type=f_type).encode())
                        # Sending the content
                        client.send(content.encode())

                except FileNotFoundError:
                    # Sending 404 error if the file is not found
                    client.send(resp(404).encode())

        except IndexError:
            # Sending 400 error if the request is not valid
            client.send(resp(400).encode())
