from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading

porta = 8000

def abrirSite():
    webbrowser.open("http://localhost:" + str(porta))

servidor = HTTPServer(("localhost", porta), SimpleHTTPRequestHandler)

print("================================")
print(" GABIRU PETZ ONLINE ")
print("================================")
print("Site aberto em:")
print("http://localhost:" + str(porta))

threading.Timer(1, abrirSite).start()

servidor.serve_forever()