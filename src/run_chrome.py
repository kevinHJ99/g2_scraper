import subprocess
import time
import socket

class ChromeManager:
    @staticmethod
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) == 0

    @staticmethod
    def ensure_chrome():
        if not ChromeManager.is_port_open(9222):
            subprocess.Popen([
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "--remote-debugging-port=9222",
                "--user-data-dir=C:\\chrome-automation",
                "--no-first-run",
                "--no-default-browser-check"
            ])
        time.sleep(5)