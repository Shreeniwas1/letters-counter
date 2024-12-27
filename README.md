
#  Global Letter Counter

A sophisticated real-time letter tracking application that monitors your typing activity and provides detailed analytics through interactive graphs.

[Letter Counter Demo]

![image](https://github.com/user-attachments/assets/7e3e923d-7eb0-419e-bb95-d8fcd5bda773)

## Features

- **Real-time Letter Counting**: Tracks alphabetic characters typed anywhere on your system
- **Live Typing Speed**: Displays current typing speed in Characters Per Minute (CPM)
- **Interactive Graphs**: 
  - Letter count over time
  - Typing speed variations
- **Dark Theme**: Easy on the eyes with a modern dark interface
- **Responsive Design**: Adapts to window resizing
- **Control Options**:
  - Start/Stop tracking
  - Reset counters
  - Real-time updates

## Requirements

- Python 3.x
- Required packages:
  ```
  tkinter
  ttkbootstrap
  pynput
  matplotlib
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/letter-counter.git
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python lettercounter.py
   ```

2. Click "Start Tracking" to begin monitoring your typing
3. Type anywhere on your system to see the counter and graphs update
4. Use "Stop Tracking" to pause monitoring
5. "Reset Counters" will clear all data and graphs

## Features in Detail

### Typing Analytics
- **Global Letter Count**: Tracks total alphabetic characters typed
- **Typing Speed**: Calculates CPM with intelligent idle time handling
- **Visual Analytics**: Real-time graphing of typing patterns

### Smart Tracking
- Tracks only alphabetic characters
- Automatically handles idle time (>10 seconds between keystrokes)
- Continuous updates with configurable refresh rate

### User Interface
- Modern dark theme using ttkbootstrap
- Responsive graph layouts
- Clear, easy-to-read statistics

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
