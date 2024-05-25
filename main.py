import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import socket
import threading
from queue import Queue
from urllib.parse import urlparse

# Número de hilos para escanear
num_threads = 50
openports = []

class PortScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("Port Scanner App")
        master.geometry("500x650")
        master.configure(bg="#f0f0f0")

        # Cabecera con título
        self.header_frame = tk.Frame(master, bg="#f0f0f0")
        self.header_frame.pack(pady=10)

        self.title_label = tk.Label(self.header_frame, text="PORT SCANNER", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack()

        # Añadir imagen lupa.jpg
        self.image = Image.open("lupa.png")
        self.image = self.image.resize((30, 30), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.header_frame, image=self.photo, bg="#f0f0f0")
        self.image_label.pack(pady=10)

        self.url_label = tk.Label(master, text="Introduce una URL:", bg="#f0f0f0")
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack(pady=5)

        self.scan_button = tk.Button(master, text="Escanear", command=self.start_scan)
        self.scan_button.pack(pady=5)

        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="indeterminate")
        self.progress_bar.pack(pady=5)

        self.result_text = tk.Text(master, wrap="word", height=15)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.result_text.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.result_text.config(yscrollcommand=self.scrollbar.set)

        self.stop_button = tk.Button(master, text="Parar Escaneo", command=self.stop_scan)
        self.stop_button.pack(pady=5)
        self.stop_button.config(state="disabled")

        self.scanning = False

    def get_host_address(self, url):
        """
        Dada una URL, devuelve la dirección IP del host.
        """
        try:
            # Analiza la URL para obtener el nombre del host
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            
            # Obtiene la dirección IP del host
            ip_address = socket.gethostbyname(host)
            return ip_address
        except Exception as e:
            return f"Error al obtener la dirección IP: {e}"

    def port_scan(self, port, target_host):
        """
        Escanea un puerto en el host especificado.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Desconocido"
                self.result_text.insert(tk.END, f"Puerto {port}: Abierto ({service})\n")
                openports.append(port)
            else:
                self.result_text.insert(tk.END, ".")
            sock.close()
        except socket.error as err:
            self.result_text.insert(tk.END, f"Error al escanear el puerto {port}: {err}\n")

    def threader(self, target_host):
        while not self.stop_event.is_set():
            worker = port_queue.get()
            self.port_scan(worker, target_host)
            port_queue.task_done()
        self.scanning = False
        self.scan_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_bar.stop()

    def start_scan(self):
        self.scanning = True
        self.stop_event = threading.Event()
        self.stop_button.config(state="normal")
        self.scan_button.config(state="disabled")
        self.progress_bar.start()
        url = self.url_entry.get()
        target_host = self.get_host_address(url)
        if "Error" in target_host:
            self.result_text.insert(tk.END, target_host)
            return

        self.result_text.insert(tk.END, f"Escaneando host: {target_host}\n")

        start_port = 79
        end_port = 9091

        # Cola de puertos para escanear
        global port_queue
        port_queue = Queue()

        for worker in range(start_port, end_port + 1):
            port_queue.put(worker)
        
        # Ejecutar el escaneo de puertos en un hilo secundario
        scan_thread = threading.Thread(target=self.threader, args=(target_host,))
        scan_thread.start()

    def stop_scan(self):
        if self.scanning:
            self.stop_event.set()

def main():
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
