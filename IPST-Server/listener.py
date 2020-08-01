import base64
import selectors
import socket
import types
import tileLoc

class listener:
    def accept_client_socket(self, listener_socket):
        client_socket, client_address = listener_socket.accept()
        print("Accepted connection from", client_address)
        client_socket.setblocking(False)
        client_data = types.SimpleNamespace(client_address = client_address, input_buffer = "", output_buffer = "", photo = False)
        client_events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.listener_selectors.register(client_socket, client_events, data = client_data)

    def handle_client_service(self, key, event):
        client_socket = key.fileobj
        client_data = key.data

        if event & selectors.EVENT_READ:
            try:
                input_data = client_socket.recv(1024)
                if input_data:
                    input_string = input_data.decode("utf-8")

                    # STORE #
                    if (client_data.photo and input_string[-5:] == "STORE"):
                        if client_data.input_buffer[:5] == "STORE":
                            fifth_semicolon = input_string.rfind(";")
                            forth_semicolon = input_string[:fifth_semicolon].rfind(";")
                            third_semicolon = input_string[:forth_semicolon].rfind(";")
                            second_semicolon = input_string[:third_semicolon].rfind(";")
                            first_semicolon = input_string[:second_semicolon].rfind(";")

                            if first_semicolon > second_semicolon or second_semicolon > third_semicolon or third_semicolon > forth_semicolon or forth_semicolon > fifth_semicolon:
                                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                                client_data.output_buffer = "STOREDAMAGED1STORE".encode("ascii")
                                print("STORE DAMAGED1")
                            else:
                                client_data.photo = False
                                client_data.input_buffer += input_string[:first_semicolon]

                                name = input_string[first_semicolon + 1:second_semicolon]
                                x = input_string[second_semicolon + 1:third_semicolon]
                                y = input_string[third_semicolon + 1:forth_semicolon]
                                a = input_string[forth_semicolon + 1:fifth_semicolon]
                                image = base64.b64decode(client_data.input_buffer[5:])

                                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                                client_data.output_buffer = tileLoc.store_feature(image, name, x, y, a).encode("ascii")
                                print("STORE DONE")
                        else:
                            client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                            client_data.output_buffer = "STOREDAMAGED2STORE".encode("ascii")
                            print("STORE DAMAGED2")
                    elif (not client_data.photo and input_string[:5] == "STORE"):
                        client_data.photo = True
                        client_data.input_buffer += input_string

                    # RESTORE #
                    elif (input_string[:7] == "RESTORE"):
                        # tileLoc.show_all_feature()
                        client_data.output_buffer = tileLoc.restore_feature().encode("ascii")
                        print("RESTORE DONE")
                    
                    # MATC1 #
                    elif (client_data.photo and input_string[-5:] == "MATC1"):
                        if client_data.input_buffer[:5] == "MATC1":
                            second_semicolon = input_string.rfind(";")
                            first_semicolon = input_string[:second_semicolon].rfind(";")

                            if first_semicolon > second_semicolon:
                                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                                client_data.output_buffer = "MATCHDAMAGED1MATCH".encode("ascii")
                                print("MATC1 DAMAGED1")
                            else:
                                client_data.photo = False
                                client_data.input_buffer += input_string[:first_semicolon]

                                a = float(input_string[first_semicolon + 1:second_semicolon])
                                image = base64.b64decode(client_data.input_buffer[5:])
                                tileLoc.matc0(image, a)
                                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                                client_data.output_buffer = "MATCHX100Y60,10598.3545,7462.455;MATCH".encode("ascii")
                                print("MATC1 DONE")
                        else:
                            client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                            client_data.output_buffer = "MATCHDAMAGED2MATCH".encode("ascii")
                            print("MATC1 DAMAGED2")
                    elif (not client_data.photo and input_string[:5] == "MATC1"):
                        client_data.photo = True
                        client_data.input_buffer += input_string

                    # MATC2 #
                    elif (client_data.photo and input_string[-5:] == "MATC2"):
                        if client_data.input_buffer[:5] == "MATC2":
                            second_semicolon = input_string.rfind(";")
                            first_semicolon = input_string[:second_semicolon].rfind(";")

                            if first_semicolon > second_semicolon:
                                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                                client_data.output_buffer = "MATCHDAMAGED1MATCH".encode("ascii")
                                print("MATC2 DAMAGED1")
                            else:
                                client_data.photo = False
                                client_data.input_buffer += input_string[:first_semicolon]

                                a = input_string[first_semicolon + 1:second_semicolon]
                                image = base64.b64decode(client_data.input_buffer[5:])
                                tileLoc.matc2(image)
                                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                                client_data.output_buffer = "MATCHX100Y60,10598.3545,7462.455;MATCH".encode("ascii")
                                print("MATC2 DONE")
                        else:
                            client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                            client_data.output_buffer = "MATCHDAMAGED2MATCH".encode("ascii")
                            print("MATC2 DAMAGED2")
                    elif (not client_data.photo and input_string[:5] == "MATC2"):
                        client_data.photo = True
                        client_data.input_buffer += input_string

                    # MATCH #
                    elif (client_data.photo and input_string[-5:] == "MATCH"):
                        if client_data.input_buffer[:5] == "MATCH":
                            second_semicolon = input_string.rfind(";")
                            first_semicolon = input_string[:second_semicolon].rfind(";")

                            if first_semicolon > second_semicolon:
                                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                                client_data.output_buffer = "MATCHDAMAGED1MATCH".encode("ascii")
                                print("MATCH DAMAGED1")
                            else:
                                client_data.photo = False
                                client_data.input_buffer += input_string[:first_semicolon]

                                a = input_string[first_semicolon + 1:second_semicolon]
                                image = base64.b64decode(client_data.input_buffer[5:])

                                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                                client_data.output_buffer = tileLoc.match_feature(image, a).encode("ascii")
                                print("MATCH DONE")
                        else:
                            client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                            client_data.output_buffer = "MATCHDAMAGED2MATCH".encode("ascii")
                            print("MATCH DAMAGED2")
                    elif (not client_data.photo and input_string[:5] == "MATCH"):
                        client_data.photo = True
                        client_data.input_buffer += input_string

                    # STORE and MATCH #
                    elif (client_data.photo):
                        client_data.input_buffer += input_string
                else:
                    print('Closing connection to', client_data.client_address)
                    self.listener_selectors.unregister(client_socket)
                    client_socket.close()
            except ConnectionResetError:
                client_data.photo = False
                client_data.input_buffer = client_data.input_buffer[len(client_data.input_buffer):]
                print("[WinError 10054] 遠端主機已強制關閉一個現存的連線。")
        if event & selectors.EVENT_WRITE:
            if client_data.output_buffer:
                sent = client_socket.send(client_data.output_buffer)
                client_data.output_buffer = client_data.output_buffer[sent:]

    def start(self, ip, port):
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_selectors = selectors.DefaultSelector()
        self.listener_socket.bind((ip, port))
        self.listener_socket.listen()
        self.listener_socket.setblocking(False)
        self.listener_selectors.register(self.listener_socket, selectors.EVENT_READ, data = None)

        print("Listener started")

        while True:
            events = self.listener_selectors.select(timeout = None)
            for key, event in events:
                if key.data is None:
                    self.accept_client_socket(key.fileobj)
                else:
                    self.handle_client_service(key, event)