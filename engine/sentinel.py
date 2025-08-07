import subprocess
import os
import time

def start_backend():
    print("Iniciando o backend FastAPI...")
    # Certifique-se de que o diretório de trabalho está correto para o uvicorn encontrar main.py
    process = subprocess.Popen(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"], cwd="./engine/backend")
    return process

if __name__ == "__main__":
    backend_process = None
    try:
        backend_process = start_backend()
        print("Backend iniciado. Pressione Ctrl+C para parar.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Parando o backend...")
        if backend_process:
            backend_process.terminate()
            backend_process.wait()
        print("Backend parado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        if backend_process:
            backend_process.terminate()
            backend_process.wait()


