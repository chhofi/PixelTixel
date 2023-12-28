import socket
import time
import random
from PIL import Image
import logging

# Server-Adresse und Port
HOST = '151.217.15.90'
PORT = 1337

# Modusauswahl: 'square' oder 'image'
mode = 'square'  # Ändere dies zu 'image', um ein Bild zu zeichnen

# Mittelpunkt definieren
MID_X = 1300  # Mittelpunkt X-Achse 1700
MID_Y = 800  # Mittelpunkt Y-Achse 

# Bild laden und Größe anpassen, falls Modus 'image' gewählt wird
if mode == 'square':
    image_path = 'cybercat.png'  # Setze den Pfad zu deinem Bild
    image = Image.open(image_path)
    image = image.resize((200, 200))  # Größe anpassen
    image = image.convert('RGB')
    SIZE_X = image.width
    SIZE_Y = image.height
else:
    SIZE_X = 200  # Quadratgröße X
    SIZE_Y = 200  # Quadratgröße Y


# Startposition basierend auf Mittelpunkt berechnen
START_X = MID_X - SIZE_X // 2
START_Y = MID_Y - SIZE_Y // 2

# Zeichenfunktion
def draw(mode, start_x, end_x, s):
    drawn_pixels = set()  # Set to store the drawn pixels

    if mode == 'square':
        pixel_coords = [(x, y) for x in range(start_x, end_x) for y in range(START_Y, START_Y + SIZE_Y)]
        random.shuffle(pixel_coords)  # Mische die Koordinaten

        for screen_x, screen_y in pixel_coords:
            if (screen_x, screen_y) not in drawn_pixels:
                color = '00FF00'  # Farbe für das Quadrat
                pixel_data = f'PX {screen_x} {screen_y} {color}\n'
                try:
                    s.sendall(pixel_data.encode())
                except socket.error as e:
                    print(f"Socket error: {e}")
                    break  # Or handle reconnection logic here
                drawn_pixels.add((screen_x, screen_y))

    elif mode == 'image':
        pixel_coords = [(x, y) for x in range(start_x - START_X, end_x - START_X) for y in range(SIZE_Y)]
        random.shuffle(pixel_coords)  # Mische die Koordinaten

        for img_x, img_y in pixel_coords:
            if (img_x, img_y) not in drawn_pixels and 0 <= img_x < SIZE_X and 0 <= img_y < SIZE_Y:
                screen_x = img_x + START_X
                screen_y = img_y + START_Y
                r, g, b = image.getpixel((img_x, img_y))
                color = f'{r:02x}{g:02x}{b:02x}'
                pixel_data = f'PX {screen_x} {screen_y} {color}\n'
                try:
                    s.sendall(pixel_data.encode())
                except socket.error as e:
                    print(f"Socket error: {e}")
                    break  # Or handle reconnection logic here
                drawn_pixels.add((img_x, img_y))



# Anzahl der Threads
THREAD_COUNT = 1

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use a dummy address; no actual connection is made
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            return ip
    except Exception as e:
        logging.error(f"Failed to get local IP: {e}")
        return None
    
def main():
    local_ip = get_local_ip()
    if not local_ip:
        logging.error("No local IP address found. Check network connection.")
        return

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Pixelflut started ...")
                s.bind((local_ip, 0))  # Bind to the specified IP address
                s.connect((HOST, PORT))
                draw(mode, START_X, START_X + SIZE_X, s)
        except ConnectionRefusedError:
            print("Connection refused, trying again...")
            time.sleep(0.1)
        except Exception as e:
            logging.error(f"Error during drawing: {e}")
            time.sleep(1)  # Wait a bit before retrying

if __name__ == "__main__":
    main()