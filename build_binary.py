#!/usr/bin/python
import os

if __name__ == '__main__':
    cmd = 'pyinstaller --icon=./UI/icon.ico --onefile --noconsole --distpath=./bin aotas.py'
    os.system(cmd)
