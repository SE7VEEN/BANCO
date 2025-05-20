import unicodedata

import json
import os
from cliente.cuentas.cuenta2 import Cuenta

import os

# 1. __file__ apunta a BANCO/general/utils/utils.py
# 2. Subimos 3 niveles para llegar a BANCO/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 3. Construimos ruta hacia BANCO/cliente/datos
DATOS_DIR = os.path.join(BASE_DIR, 'cliente', 'datos')

# Archivos JSON dentro de cliente/datos
CUENTAS_PATH = os.path.join(DATOS_DIR, 'cuentas.json')
CLIENTES_PATH = os.path.join(DATOS_DIR, 'clientes.json')

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
