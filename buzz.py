import socket
import threading
import time
import tkinter as tk

DEFAULT_IP = "192.168.4.1"
DEFAULT_PORT = "80"
AUTO_RESET_MS = 10000


class ESP32ClientGUI:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("ESP32 TCP Client - Fullscreen Display")
        self.master.attributes("-fullscreen", True)
        self.master.configure(bg="#000000")

        self.client_socket = None
        self.connected = False
        self.data_locked = False
        self.stop_listener = threading.Event()

        self._build_ui()
        self._bind_keys()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self) -> None:
        self.team_label = tk.Label(
            self.master,
            text="Waiting...",
            bg="#000000",
            fg="white",
            font=("Arial", 220, "bold"),
        )
        self.team_label.pack(expand=True)

        bottom_frame = tk.Frame(self.master, bg="#111111")
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=15)

        tk.Label(bottom_frame, text="IP:", bg="#111111", fg="white", font=("Arial", 12)).pack(
            side=tk.LEFT, padx=5
        )
        self.ip_entry = tk.Entry(bottom_frame, font=("Arial", 12), width=15, justify="center")
        self.ip_entry.insert(0, DEFAULT_IP)
        self.ip_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(bottom_frame, text="Port:", bg="#111111", fg="white", font=("Arial", 12)).pack(
            side=tk.LEFT, padx=5
        )
        self.port_entry = tk.Entry(bottom_frame, font=("Arial", 12), width=8, justify="center")
        self.port_entry.insert(0, DEFAULT_PORT)
        self.port_entry.pack(side=tk.LEFT, padx=5)

        self.connect_btn = tk.Button(
            bottom_frame,
            text="Connect",
            font=("Arial", 12, "bold"),
            bg="#0078D7",
            fg="white",
            command=self.connect_to_esp32,
        )
        self.connect_btn.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(
            bottom_frame,
            text="Status: Disconnected",
            bg="#111111",
            fg="red",
            font=("Arial", 12),
        )
        self.status_label.pack(side=tk.LEFT, padx=15)

        self.reset_label = tk.Label(
            bottom_frame,
            text="Press [Enter] to reset | Press [Esc] to exit fullscreen",
            bg="#111111",
            fg="#888888",
            font=("Arial", 14),
        )
        self.reset_label.pack(side=tk.RIGHT, padx=15)

    def _bind_keys(self) -> None:
        self.master.bind("<Return>", self.reset_display)
        self.master.bind("<Escape>", self.exit_fullscreen)

    def connect_to_esp32(self) -> None:
        if self.connected:
            self.disconnect_esp32()
            return

        ip = self.ip_entry.get().strip()
        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            self.status_label.config(text="Invalid port number", fg="red")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)

        try:
            self.client_socket.connect((ip, port))
            self.client_socket.setblocking(False)

            self.connected = True
            self.stop_listener.clear()

            self.status_label.config(text=f"Connected to {ip}:{port}", fg="green")
            self.connect_btn.config(text="Disconnect", bg="#d9534f")

            threading.Thread(target=self.listen_for_data, daemon=True).start()
        except Exception as exc:
            self.status_label.config(text=f"Connection failed: {exc}", fg="red")
            self.client_socket = None
            self.connected = False

    def disconnect_esp32(self) -> None:
        self.stop_listener.set()

        if self.client_socket is not None:
            try:
                self.client_socket.close()
            except OSError:
                pass

        self.client_socket = None
        self.connected = False

        self.status_label.config(text="Disconnected", fg="red")
        self.connect_btn.config(text="Connect", bg="#0078D7")

    def listen_for_data(self) -> None:
        while self.connected and not self.stop_listener.is_set():
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    self.master.after(0, self.disconnect_esp32)
                    break

                msg = data.decode(errors="ignore").strip()
                if msg and not self.data_locked:
                    self.data_locked = True
                    self.master.after(0, lambda m=msg: self.display_team(m))
            except BlockingIOError:
                time.sleep(0.01)
            except OSError:
                break
            except Exception as exc:
                self.master.after(0, lambda e=exc: self.status_label.config(text=f"Error: {e}", fg="red"))
                break

    def display_team(self, msg: str) -> None:
        self.team_label.config(text=msg, fg="yellow")
        self.reset_label.config(fg="#00FF00")
        self.master.after(AUTO_RESET_MS, self.reset_display)

    def reset_display(self, event=None) -> None:
        if not self.data_locked:
            return

        self.data_locked = False
        self.team_label.config(text="Waiting...", fg="white")
        self.reset_label.config(fg="#888888")

    def exit_fullscreen(self, event=None) -> None:
        self.master.attributes("-fullscreen", False)
        self.status_label.config(text="Exited Fullscreen Mode", fg="orange")

    def on_close(self) -> None:
        self.disconnect_esp32()
        self.master.destroy()


def main() -> None:
    root = tk.Tk()
    ESP32ClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
