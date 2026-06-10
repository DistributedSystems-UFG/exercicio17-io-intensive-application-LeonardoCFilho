from const import *
import threading
import socket

def handle(conn):
    """Executado em thread própria para cada cliente."""
    with conn:
        data = conn.recv(1024).decode().strip()
        if data == "LER":
            try:
                with open(ARQUIVO_TESTE) as f:
                    conteudo = f.read()
                resp = conteudo
            except FileNotFoundError:
                resp = "ERRO: arquivo não encontrado"
        else:
            resp = "ERRO: comando desconhecido"
        conn.sendall(resp.encode())


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT_THREAD_REQ))
        srv.listen()
        print(f"[thread/req] escutando em {HOST}:{PORT_THREAD_REQ}")
        while True:
            conn, _ = srv.accept()
            t = threading.Thread(target=handle, args=(conn,), daemon=True)
            t.start()              # nova thread por requisição


if __name__ == "__main__":
    main()
