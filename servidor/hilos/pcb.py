import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from multiprocessing import Lock
from general.utils.utils import CUENTAS_PATH, PCB_PATH, inicializar_archivo

pcb_lock = Lock()
cuentas_lock = Lock()

import json
from threading import Lock

# Añade un Lock global para sincronizar el acceso al archivo
pcb_lock = Lock()

def guardar_en_pcb(proceso):
    with pcb_lock:  # Bloquea el acceso concurrente
        try:
            # Leer datos existentes
            try:
                with open(PCB_PATH, 'r') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []
            
            # Convertir a dict si es necesario
            proceso_dict = proceso.to_dict() if hasattr(proceso, 'to_dict') else proceso
            
            # Añadir nuevo proceso
            data.append(proceso_dict)
            
            # Escribir todo el array de nuevo
            with open(PCB_PATH, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            print(f"Error al guardar en PCB: {str(e)}")

# def terminar_proceso(proceso):
#     proceso.estado = "Finalizado"
#     guardar_en_pcb(proceso)

def obtener_datos_cliente(id_usuario):
    with cuentas_lock:
        try:
            inicializar_archivo(CUENTAS_PATH)
            with open(CUENTAS_PATH, 'r') as f:
                cuentas = json.load(f)
            for cuenta in cuentas:
                if cuenta.get('id_usuario') == id_usuario:
                    return cuenta
            return None
        except Exception as e:
            print(f"Error obteniendo datos del cliente: {str(e)}")
            return None
    datos_cliente = {
        'id_cuenta': 'CTA-XXXXXX',
        'tipo_cuenta': 'premium'  # o 'estandar' según corresponda
    }
    return datos_cliente
        


