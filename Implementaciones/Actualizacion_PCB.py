from multiprocessing import Process, Lock
import json, time, os, shutil, sys, datetime
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from general.utils.utils import PCB_PATH


def actualizar_estado_pcb(pid, nuevo_estado):
    pcb_lock = Lock
    with pcb_lock:
        with open(PCB_PATH, 'r+') as f:
            pcb = json.load(f)
            for p in pcb:
                if p["PID"] == pid:
                    p["Estado"] = nuevo_estado
                    p["Timestamp"] = datetime.now().strftime("%H:%M:%S")
                    break
            f.seek(0)
            json.dump(pcb, f, indent=4)
            f.truncate()
