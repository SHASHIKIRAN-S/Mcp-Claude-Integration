import subprocess
import sys

required = ['pymysql']
for pkg in required:
    try:
        __import__(pkg)
    except ImportError:
        print(f"{pkg} not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
