
from multiprocessing import Process, Lock
import threading
import json, time, os, shutil, sys, datetime
from pathlib import Path
pcb_lock = threading.Lock()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from general.utils.utils import PCB_PATH
def actualizar_estado_pcb(pid, estado=None, operacion=None, recurso_esperando=None, recurso_adquirido=None):
    with pcb_lock:
        with open(PCB_PATH, 'r+') as f:
            pcb = json.load(f)
            for p in pcb:
                if str(p["PID"]) == str(pid):
                    if estado:
                        p["Estado"] = estado
                    if operacion:
                        p["OperacionActual"] = operacion
                    if recurso_esperando:
                        p["RecursoEsperando"] = recurso_esperando
                    if recurso_adquirido:
                        p["RecursoAdquirido"] = recurso_adquirido
                    break
            f.seek(0)
            f.truncate()
            json.dump(pcb, f, indent=4)
