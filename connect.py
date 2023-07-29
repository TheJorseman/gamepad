import argparse
import socket
import logging
import keyboard
from threading import Thread

logging.basicConfig(filename="key_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Argument parsing function
def parse_args():
    parser = argparse.ArgumentParser(description='Script para enviar/recibir teclas')
    parser.add_argument('mode', type=str, choices=["send", "receive"],
                        help='Modo en que el script deberá operar (send o receive)')
    parser.add_argument('puerto', type=int,
                        help='Puerto por el cual va a estar a la escucha')
    parser.add_argument('--ip', type=str, default="0.0.0.0",
                        help='IP a la que se podria conectar si esta en modo send')

    return parser.parse_args()

def on_press(event):
    if args.mode == 'send':
        try:
            key = event.name
            client.send(key.encode())
            logging.info(str(key))
        except NameError:
            print("La variable 'client' no está definida. Asegúrese de que el cliente esté conectado antes de intentar enviar datos.")

def handle_client(client):
    while True:
        data = client.recv(1024)
        if not data:
            break
        key = data.decode()
        keyboard.press_and_release(key)
        logging.info(key)

# Main function
def main():
    global client
    global args
    args = parse_args()

    if args.mode == 'receive':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((args.ip, args.puerto))
        server.listen()
        print(f"Escuchando en {args.ip}:{args.puerto}")

        while True:
            client, addr = server.accept()
            print(f"Conexión desde {addr}")
            Thread(target=handle_client, args=(client,)).start()

    else:  # Modo send
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((args.ip, args.puerto))
        keyboard.on_press(on_press)

        # Block forever to keep the script running
        keyboard.wait()

if __name__ == "__main__":
    main()
