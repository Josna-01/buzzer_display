# ESP32 Buzzer Display Client (`buzzer_final2`)

Fullscreen Python GUI client that connects to an ESP32 TCP server and displays incoming team numbers/messages for event workflows.

## Features

- Fullscreen high-visibility display for stage/event use
- TCP client connection to ESP32 (default: `192.168.4.1:80`)
- Connect/Disconnect control from GUI
- Auto-reset display after 10 seconds
- Manual reset with `Enter`
- Exit fullscreen with `Esc`
- Non-blocking socket listener thread

## Project Files

- `buzz.py`: Main application source code
- `buzz.spec`: PyInstaller build configuration
- `buzzer.ico`: Application icon
- `buzzer-display-client-documentation.md`: Full project documentation

## Requirements

- Python 3.9+
- Tkinter (usually bundled with standard Python on Windows)

Install optional packaging tool:

```bash
pip install -r requirements.txt
```

## Run (Source)

```bash
python buzz.py
```

## Build EXE (PyInstaller)

```bash
pyinstaller buzz.spec
```

Built output is generated under `dist/`.

## Usage Flow

1. Launch app.
2. Enter ESP32 IP and port (or keep defaults).
3. Click `Connect`.
4. Incoming TCP text is displayed in large yellow text.
5. Display auto-resets after timeout, or press `Enter` to reset manually.

## Notes

- Designed for LAN/AP network where ESP32 acts as TCP server.
- If connection drops, the app updates status and allows reconnect.

## License

MIT License. See `LICENSE`.

