from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading


# Porta do site
PORTA = 8000


# Função para abrir navegador
def abrir_navegador():
    webbrowser.open(f"http://localhost:{PORTA}")


# Configuração do servidor
servidor = HTTPServer(
    ("localhost", PORTA),
    SimpleHTTPRequestHandler
)

print("=" * 40)
print("🐾 GABIRU PETZ ONLINE")
print("=" * 40)

print(f"Site aberto em:")
print(f"http://localhost:{PORTA}")


# Abre o navegador automaticamente
threading.Timer(1, abrir_navegador).start()


# Inicia servidor
servidor.serve_forever()