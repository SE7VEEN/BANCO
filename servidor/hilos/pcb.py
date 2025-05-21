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

import json, time
import threading
from pathlib import Path
from atomicwrites import atomic_write

pcb_lock = threading.Lock()


def guardar_en_pcb(proceso):
    with pcb_lock:
        try:
            # 1. Obtener ruta absoluta confiable
            base_dir = Path(__file__).resolve().parent.parent.parent
            datos_dir = base_dir / "general" / "datos"
            pcb_path = datos_dir / "pcb.json"
            
            # 2. Crear directorios si no existen
            datos_dir.mkdir(parents=True, exist_ok=True)
            
            # 3. Cargar datos existentes o inicializar
            try:
                if pcb_path.exists():
                    data = json.loads(pcb_path.read_text(encoding='utf-8'))
                else:
                    data = []
            except json.JSONDecodeError:
                data = []
            
            # 4. Validar estructura de datos
            if not isinstance(data, list):
                data = []
            
            # 5. Añadir nuevo proceso
            new_entry = proceso.to_dict()
            new_data = data + [new_entry]
            
            # 6. Escritura atómica con manejo de errores
            try:
                with atomic_write(pcb_path, overwrite=True, encoding='utf-8') as f:
                    json.dump(new_data, f, indent=4, ensure_ascii=False)
            except PermissionError:
                # Esperar y reintentar una vez
                time.sleep(0.1)
                with atomic_write(pcb_path, overwrite=True, encoding='utf-8') as f:
                    json.dump(new_data, f, indent=4, ensure_ascii=False)
                    
        except Exception as e:
            print(f"Error al guardar PCB: {type(e).__name__} - {str(e)}")
            # Crear archivo vacío como último recurso
            if not datos_dir.exists():
                datos_dir.mkdir(parents=True)
            pcb_path.write_text('[]', encoding='utf-8')

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
        


