import subprocess
import platform
import logging
import time
import shutil
import winreg
import socket

class ChromeManager:
        
    @staticmethod
    def find_chrome():
        system = platform.system()

        path = shutil.which("chrome") or \
        shutil.which("google-chrome") or \
        shutil.which("chrome.exe")

        if path:
            return path

        if system == "Windows":
            path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
            for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                try:
                    with winreg.OpenKey(root, path) as key:
                        return winreg.QueryValue(key, None)
                except FileNotFoundError:
                    continue
            return None
    
    @staticmethod
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) == 0

    @staticmethod
    def ensure_chrome():
        chrome_path = None

        find_chrome_path = ChromeManager.find_chrome()

        if not find_chrome_path:
            logging.error("Google Chrome path could not be found.")
        else:
            chrome_path = find_chrome_path

        if not ChromeManager.is_port_open(9222):
            subprocess.Popen([
                chrome_path,
                "--remote-debugging-port=9222",
                "--user-data-dir=C:\\chrome-automation",
                "--no-first-run",
                "--no-default-browser-check"
            ])
        time.sleep(5)