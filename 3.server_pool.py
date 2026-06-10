from concurrent.futures import ThreadPoolExecutor
from const import *
import socket

POOL_SIZE = 10          # tamanho fixo do pool

def handle(conn):
    """Tarefa submetida ao pool para cada conexão."""
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
    with ThreadPoolExecutor(max_workers=POOL_SIZE) as pool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((HOST, PORT_THREAD_POOL))
            srv.listen()
            print(f"[pool/{POOL_SIZE}] escutando em {HOST}:{PORT_THREAD_POOL}")
            while True:
                conn, _ = srv.accept()
                pool.submit(handle, conn)   # delega ao pool


if __name__ == "__main__":
    main()
