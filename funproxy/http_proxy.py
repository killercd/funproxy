import socket
import threading
import ssl

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8888

def handle_https(client_socket, addr, server_host, server_port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server_host, server_port))

        client_socket.send(b"HTTP/1.1 200 Connection established\r\n\r\n")

        client_socket.setblocking(0)
        server_socket.setblocking(0)

        while True:
            try:
                data_from_client = client_socket.recv(4096)
                if len(data_from_client) > 0:
                    server_socket.send(data_from_client)
            except:
                pass

            try:
                data_from_server = server_socket.recv(4096)
                if len(data_from_server) > 0:
                    client_socket.send(data_from_server)
            except:
                pass

    except Exception as e:
        print(f"Errore HTTPS (CONNECT): {e}")
    finally:
        client_socket.close()
        server_socket.close()

def handle_http(client_socket, addr):
    try:
        request = client_socket.recv(4096)

        request_line = request.split(b'\n')[0]
        url = request_line.split(b' ')[1]

        http_pos = url.find(b'://')
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(b':') 
        server_pos = temp.find(b'/')
        if server_pos == -1:
            server_pos = len(temp)

        if port_pos == -1 or server_pos < port_pos:
            port = 80  # 
            server_host = temp[:server_pos]
        else:
            port = int(temp[(port_pos + 1):][:server_pos - port_pos - 1])
            server_host = temp[:port_pos]

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server_host.decode('utf-8'), port))

        server_socket.send(request)

        while True:
            response = server_socket.recv(4096)
            if len(response) > 0:
                client_socket.send(response)
            else:
                break

        server_socket.close()
        client_socket.close()

    except Exception as e:
        print(f"Errore HTTP: {e}")
        client_socket.close()

def handle_client(client_socket, addr):
    try:
        request = client_socket.recv(4096)
        first_line = request.split(b'\n')[0].decode()

        if first_line.startswith("CONNECT"):
            server_host_port = first_line.split(' ')[1]
            server_host, server_port = server_host_port.split(':')
            server_port = int(server_port)

            handle_https(client_socket, addr, server_host, server_port)
        else:
            handle_http(client_socket, addr)

    except Exception as e:
        print(f"Errore durante la gestione della richiesta: {e}")
        client_socket.close()

def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(5)

    print(f"Proxy in ascolto su {PROXY_HOST}:{PROXY_PORT}")

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"Connessione ricevuta da {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_proxy()
