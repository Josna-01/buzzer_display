# ARC SJEC - ESP32 TCP Fullscreen Display Client (Python Tkinter)
## Project Documentation

---

## 1. Project Title Page

| Field | Details |
|---|---|
| **Project Title** | ESP32 TCP Fullscreen Display Client for Buzzer/Event Calls |
| **Developed By** | Members of ARC-SJEC |
| **Club** | Automation and Robotics Club (ARC-SJEC) |
| **Institution** | St. Joseph Engineering College (SJEC), Mangaluru |
| **Department** | Electronics / Robotics |
| **Year** | 2025-2026 |

---

## 2. Abstract

This project implements a Python-based fullscreen display client that connects to an ESP32 over TCP and shows incoming messages (for example, team numbers) in a large, high-visibility interface. The application is designed for buzzer rounds, technical events, and stage coordination where rapid and clear visual communication is needed.

The software is built using Tkinter for GUI and Python sockets for network communication. It supports connect/disconnect control, non-blocking data listening, automatic display reset after a fixed interval, and keyboard shortcuts for operator convenience.

---

## 3. Problem Statement

In event control rooms and buzzer-style competitions, operators often need to display incoming numbers quickly and clearly. Manual whiteboard updates or low-visibility screens create delays and confusion.

A lightweight system was needed that:

- Receives data in real time from ESP32.
- Displays messages fullscreen for audience visibility.
- Supports quick reset and reconnect operations.
- Runs reliably on standard Windows laptops.

---

## 4. Objectives

1. Connect to ESP32 TCP server using configurable IP and port.
2. Display received text prominently in fullscreen mode.
3. Prevent repeated overwrite until explicit/auto reset.
4. Provide simple operator controls for reset and fullscreen exit.
5. Ensure stable runtime with non-blocking socket handling.
6. Support executable packaging for easy deployment.

---

## 5. System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                              INPUT                               │
│                     ESP32 TCP Socket Messages                     │
│                     (team number / event token)                   │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ TCP/IP
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                     CONTROLLER / PROCESSING                      │
│                   Python Application (Tkinter GUI)               │
│                                                                  │
│ - Connect/disconnect socket handling                              │
│ - Background listener thread                                      │
│ - Data lock and reset logic                                       │
│ - UI status updates                                                │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                              OUTPUT                              │
│                     Fullscreen Visual Display                     │
│                 Large yellow text + connection status             │
└──────────────────────────────────────────────────────────────────┘
```

| Layer | Components |
|---|---|
| Input | TCP message from ESP32 server |
| Controller | Python socket + Tkinter UI logic |
| Output | Fullscreen message display |
| Operator UI | Connect/Disconnect, Enter reset, Esc fullscreen toggle |

---

## 6. Components Used

### 6.1 Software Stack

| # | Component | Purpose |
|---|---|---|
| 1 | Python 3.x | Runtime environment |
| 2 | Tkinter | GUI framework |
| 3 | `socket` | TCP communication |
| 4 | `threading` | Background listener execution |
| 5 | PyInstaller | Optional EXE packaging |

### 6.2 Hardware Context

| # | Component | Purpose |
|---|---|---|
| 1 | Laptop/PC (Windows) | Display terminal host |
| 2 | ESP32 | TCP server source device |
| 3 | Local network / ESP32 AP | Data transport medium |

---

## 7. Application Interface

### 7.1 Main UI Elements

- Large center text label (`Waiting...` by default).
- IP input box (default `192.168.4.1`).
- Port input box (default `80`).
- `Connect` / `Disconnect` button.
- Status label (connected/disconnected/error state).
- Instruction strip for keyboard shortcuts.

### 7.2 Keyboard Controls

| Key | Action |
|---|---|
| `Enter` | Reset display to `Waiting...` |
| `Esc` | Exit fullscreen mode |

---

## 8. Software / Code Structure

### 8.1 Core Class

| Class | Responsibility |
|---|---|
| `ESP32ClientGUI` | UI setup, connection management, listener handling, display control |

### 8.2 Important Runtime States

| Variable | Role |
|---|---|
| `connected` | Active socket connection status |
| `data_locked` | Prevents repeated overwrite before reset |
| `stop_listener` | Thread stop signal for clean disconnect |
| `client_socket` | TCP client instance |

### 8.3 Main Functional Methods

| Method | Description |
|---|---|
| `connect_to_esp32()` | Validates input and establishes socket connection |
| `disconnect_esp32()` | Closes socket and restores disconnected state |
| `listen_for_data()` | Reads incoming data in non-blocking background loop |
| `display_team(msg)` | Displays message and starts auto-reset timer |
| `reset_display()` | Clears current displayed message lock |
| `exit_fullscreen()` | Leaves fullscreen mode |
| `on_close()` | Graceful shutdown handler |

---

## 9. Working Principle

1. Operator launches the application.
2. App opens in fullscreen and waits in disconnected state.
3. Operator enters IP/port and clicks `Connect`.
4. Background listener waits for incoming TCP message.
5. On data receive:
   - Message appears in large yellow text.
   - Display locks to avoid rapid overwrite.
   - Auto-reset timer restores `Waiting...` after timeout.
6. Operator may manually reset using `Enter`.
7. On disconnect/error, status updates and reconnect remains available.

---

## 10. Results / Output

### 10.1 Functional Validation

| Test Case | Expected Result | Status |
|---|---|---|
| App startup | Fullscreen GUI opens | Successful |
| Valid IP/Port connect | Status turns connected | Successful |
| Data reception | Message displayed in center | Successful |
| Auto reset | Display returns to `Waiting...` | Successful |
| Manual reset (`Enter`) | Immediate display reset | Successful |
| Escape key | Fullscreen exits | Successful |
| Disconnect flow | Socket closes and status updates | Successful |

### 10.2 Packaging Validation

- PyInstaller spec present (`buzz.spec`).
- Build artifacts generated successfully (`build/`, `dist/`).

---

## 11. Technical Review - Correctness Assessment

| # | Observation | Status |
|---|---|---|
| 1 | Non-blocking socket listener avoids UI freeze | Correct |
| 2 | Threaded receive model supports continuous updates | Correct |
| 3 | Display lock prevents uncontrolled rapid updates | Correct |
| 4 | Input validation for port improves reliability | Correct |
| 5 | Clean disconnect path and window-close handling implemented | Correct |
| 6 | `build/` and `dist/` are generated artifacts and should not be versioned in source repo | GitHub hygiene note |

**Overall verdict:** The project is operational, event-ready, and suitable for deployment as both Python script and packaged executable.

---

## 12. Applications

- Buzzer round number display.
- Team call display in technical events.
- Stage queue/token display.
- Control-room visual signal terminal.
- LAN-based low-latency message display setups.

---

## 13. Future Improvements

| # | Improvement | Description |
|---|---|---|
| 1 | Reconnect Retry Logic | Automatic timed reconnect on link drop |
| 2 | Message Queue Mode | Show multiple incoming messages in sequence |
| 3 | Timestamp Overlay | Optional receive-time display |
| 4 | Theming Controls | Operator-selectable font/color presets |
| 5 | Secondary Monitor Targeting | Choose display screen in multi-monitor setups |
| 6 | Audio Alert | Short beep on new message arrival |
| 7 | Config File Support | Persist default IP/port and display options |
| 8 | Health Indicator | Packet count and connection quality display |

---

## 14. Conclusion

The `buzzer_final2` client successfully delivers a practical fullscreen TCP display interface for ESP32-driven event workflows. Its simple control model, high-visibility rendering, and dependable socket handling make it effective for hackathons, buzzer rounds, and fast-paced technical events.

With future enhancements in auto-reconnect, queuing, and configuration management, this application can scale into a robust event operations display tool.

---

*Documentation prepared for ARC-SJEC project records | St. Joseph Engineering College, Mangaluru*