#  coding: utf-8 
import re
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Urvi Patel
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK\r\n",'utf-8'))

        # get input data and separate it
        split_data = self.data.decode().split("\r\n")
        request_data = split_data[0].split(" ")
        request_type = request_data[0]
        file_path = request_data[1]

        # check request type
        if request_type == "GET":
            # check for valid file paths

            if file_path[:3] == "/..":
                # check if trying to access files above current directory
                response_text = "HTTP/1.1 404 Not Found\r\n"

            elif file_path[-1] == "/":
                # go to index.html
                file_name = "./www"+file_path+"index.html"
                try:
                    content = self.getContent(file_name)
                    response_text = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{}".format(content)
                except:
                    response_text = "HTTP/1.1 404 Not Found\r\n"

            elif file_path[-5:] == ".html":
                # open html file
                file_name = "./www"+file_path
                try:
                    content = self.getContent(file_name)
                    response_text = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{}".format(content)
                except:
                    response_text = "HTTP/1.1 404 Not Found\r\n"

            elif file_path[-4:] == ".css":
                # open css file
                file_name = "./www"+file_path
                try:
                    content = self.getContent(file_name)
                    response_text = "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n{}".format(content)
                except:
                    response_text = "HTTP/1.1 404 Not Found\r\n"

            else:
                # invalid path, 301 error and redirect
                file_name = "./www"+file_path+"/index.html"
                try:
                    content = self.getContent(file_name)
                    response_text = "HTTP/1.1 301 Moved Permanently\r\nLocation: {}\r\n".format(file_path+"/")
                except:
                    response_text = "HTTP/1.1 404 Not Found\r\n"

        else:
            # invalid method, 405 Error
            response_text = "HTTP/1.1 405 Method Not Allowed"

        # send status codes and content
        self.request.sendall(bytearray(response_text, 'utf-8'))
        return

    def getContent(self, name):
        # get file contents
        f = open(name, "r")
        content = f.read()
        f.close()

        return content


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
