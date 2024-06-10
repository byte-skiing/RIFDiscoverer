import threading
import subprocess
from subprocess import check_output

def run_command(command):
    output = check_output(command, shell=True)
    decoded_output = output.decode('cp850')
    return decoded_output

def load_emulator():
    subprocess.Popen(["/opt/genymobile/genymotion/player", "--vm-name", "Samsung A50"])
    # pid = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']).pid

if __name__ == '__main__':
    thread = threading.Thread(target=load_emulator)
    thread.start()
    thread.join()
