from const import *
import threading
import socket
import time

NUM_TESTES = 10 # Qtd de vezes que é testado tudo
TOTAL_REQUESTS = 10_000 # total de requisições por servidor
CONCURRENCY = 50 # requisições simultâneas

SERVERS = [
    ("Single-Threaded", "127.0.0.1", PORT_SINGLE_THREAD),
    ("Thread por Req", "127.0.0.1", PORT_THREAD_REQ),
    ("Pool de Threads", "127.0.0.1", PORT_THREAD_POOL),
]

def single_request(host, port, results, idx):
    # Executa a operação de leitura 1 vez, independente do modo
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=10) as s:
            s.sendall(b"LER")
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
        results[idx] = time.perf_counter() - start
    except Exception as e:
        results[idx] = None
        print(f"erro: {e}")

def benchmark(label, host, port):
    print(f"Executando: {label}")

    latencies = [None] * TOTAL_REQUESTS
    start = time.perf_counter()

    # dispara TOTAL_REQUESTS em lotes de CONCURRENCY
    for batch_start in range(0, TOTAL_REQUESTS, CONCURRENCY):
        batch_end = min(batch_start + CONCURRENCY, TOTAL_REQUESTS)
        threads = []
        for i in range(batch_start, batch_end):
            t = threading.Thread(
                target=single_request,
                args=(host, port, latencies, i),
                daemon=True,
            )
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elapsed = time.perf_counter() - start
    valid = [l for l in latencies if l is not None]

    errors = TOTAL_REQUESTS - len(valid)
    rps = len(valid) / elapsed

    return (rps, errors)


def main():
    print("\n*** BENCHMARK DE SERVIDORES ***")
    results = {}
    for i in range(NUM_TESTES):
        print("-"*25,f" ITERAÇÂO {i+1} ","-"*25)
        for label, host, port in SERVERS:
            results[label] = benchmark(label, host, port)

    print("-"*25,f" RESUMO ","-"*25)
    
    print(f"Testes rodados: {NUM_TESTES}")
    print(f"Qtd. requests por teste: {TOTAL_REQUESTS}")

    print("Single-Threaded")
    print(f"Capacidade de vazão: {results["Single-Threaded"][0]:.1f}")
    print(f"Qtd. erros: {results["Single-Threaded"][1]}")

    print("Thread por Req")
    print(f"Capacidade de vazão: {results["Thread por Req"][0]:.1f}")
    print(f"Qtd. erros: {results["Thread por Req"][1]}")

    print("Pool de Threads")
    print(f"Capacidade de vazão: {results["Pool de Threads"][0]:.1f}")
    print(f"Qtd. erros: {results["Pool de Threads"][1]}")

if __name__ == "__main__":
    main()
