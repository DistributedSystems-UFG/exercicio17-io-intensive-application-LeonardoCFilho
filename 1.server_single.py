from const import *
import socket

def handle(conn):
    """Lê o pedido, retorna as linhas do arquivo."""
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
        srv.bind((HOST, PORT_SINGLE_THREAD))
        srv.listen()
        print(f"[single] escutando em {HOST}:{PORT_SINGLE_THREAD}")
        while True:
            conn, _ = srv.accept()
            handle(conn)           # bloqueia até terminar


if __name__ == "__main__":
    main()
