import unicodedata

import json
import os
from cliente.cuentas.cuenta2 import Cuenta
from servidor.hilos.models import Proceso
from multiprocessing import Lock

pcb_lock = Lock()
cuentas_lock = Lock()

# Ruta absoluta al archivo pcb.json dentro de banco/general/datos/


import os

# 1. __file__ apunta a BANCO/general/utils/utils.py
# 2. Subimos 3 niveles para llegar a BANCO/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 3. Construimos ruta hacia BANCO/general/datos
DATOS_DIR = os.path.join(BASE_DIR, 'general', 'datos')

# Archivos JSON dentro de cliente/datos
CUENTAS_PATH = os.path.join(DATOS_DIR, 'cuentas.json')
CLIENTES_PATH = os.path.join(DATOS_DIR, 'clientes.json')
PCB_PATH = os.path.join(DATOS_DIR, 'pcb.json')

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

def formatear_telefono(numero):
    digitos = ''.join(filter(str.isdigit, numero))
    if len(digitos) >= 10:
        return f"{digitos[-10:-7]}-{digitos[-7:-4]}-{digitos[-4:]}"
    else:
        return numero

def cargar_cuentas():
    if os.path.exists(CUENTAS_PATH):
        with open(CUENTAS_PATH, 'r') as f:
            try:
                return [Cuenta.from_dict(c) for c in json.load(f)]
            except json.JSONDecodeError:
                return []
    return []

def guardar_cuentas(cuentas):
    os.makedirs(os.path.dirname(CUENTAS_PATH), exist_ok=True) 
    with open(CUENTAS_PATH, 'w') as f:
        json.dump([c.to_dict() for c in cuentas], f, indent=4)


def inicializar_archivo(filename, default=[]):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default, f)

def guardar_en_pcb(proceso):
    with pcb_lock:
        inicializar_archivo(PCB_PATH)
        with open(PCB_PATH, 'r+') as f:
            try:
                pcb = json.load(f)
            except json.JSONDecodeError:
                pcb = []
            pcb.append(proceso.to_dict())
            f.seek(0)
            json.dump(pcb, f, indent=4)
            f.truncate()  # Limpia el archivo si el nuevo JSON es más corto que el anterior

def obtener_datos_cliente(id_usuario):
    with cuentas_lock:
        inicializar_archivo(CUENTAS_PATH)
        with open(CUENTAS_PATH, 'r') as f:
            try:
                cuentas = json.load(f)
            except json.JSONDecodeError:
                return None
        for cuenta in cuentas:
            if cuenta.get('id_usuario') == id_usuario:
                return cuenta
    return None


