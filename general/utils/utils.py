import unicodedata

import json
import os
from cliente.cuentas.cuenta2 import Cuenta
from servidor.hilos.models import Proceso
from multiprocessing import Lock

pcb_lock = Lock()
cuentas_lock = Lock()

# Subimos dos niveles desde este archivo (por ejemplo, desde cliente/cuentas/gestion_cuenta.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Ruta hacia la carpeta general/datos
DATOS_PATH = os.path.join(BASE_DIR, 'general', 'datos')

# Rutas de archivos
CUENTAS_PATH = os.path.join(DATOS_PATH, 'cuentas.json')
CLIENTES_PATH = os.path.join(DATOS_PATH, 'clientes.json')

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
