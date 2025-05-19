import json
import os
from multiprocessing import Lock

pcb_lock = Lock()
cuentas_lock = Lock()

def inicializar_archivo(filename, default=[]):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default, f)

def guardar_en_pcb(proceso):
    from models import Proceso
    with pcb_lock:
        inicializar_archivo('pcb.json')
        with open('pcb.json', 'r+') as f:
            pcb = json.load(f)
            pcb.append(proceso.to_dict())
            f.seek(0)
            json.dump(pcb, f, indent=4)

def obtener_datos_cliente(id_usuario):
    with cuentas_lock:
        inicializar_archivo('cuentas.json')
        with open('cuentas.json', 'r') as f:
            cuentas = json.load(f)
        for cuenta in cuentas:
            if cuenta.get('id_usuario') == id_usuario:
                return cuenta
    return None
