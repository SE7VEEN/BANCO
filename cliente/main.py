import sys
import os
import shutil
from pathlib import Path
import json

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent  # Apunta a BANCO/
DATOS_DIR = BASE_DIR / "general" / "datos"

def limpiar_y_crear_datos():
    try:
        # Eliminar la carpeta si existe
        if DATOS_DIR.exists():
            shutil.rmtree(DATOS_DIR)
        
        # Crear la carpeta nuevamente
        DATOS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Crear archivos JSON vacíos
        archivos_necesarios = ['clientes.json', 'cuentas.json', 'pcb.json']
        for archivo in archivos_necesarios:
            with open(DATOS_DIR / archivo, 'w') as f:
                json.dump([], f)
            
        return True
    except Exception as e:
        print(f"✖ Error al limpiar datos: {str(e)}")
        return False

# Añade el directorio padre al path de Python
sys.path.append(str(BASE_DIR))

from cliente.clientes.clientes import Client
from cliente.clientes.gestor import gestionar_clientes
from cliente.cuentas.gestion_cuenta import crear_cuentas_automaticamente_por_clientes

if __name__ == "__main__":
    # Paso 1: Limpiar y crear estructura de datos
    if not limpiar_y_crear_datos():
        sys.exit(1)  # Salir si hay error
    print("\n")
    # Paso 2: Ejecutar operaciones normales
    cliente_aleatorio = Client()
    gestionar_clientes('agregar', cliente=cliente_aleatorio)
    gestionar_clientes('eliminar', id_usuario=9819)
    gestionar_clientes('generar', nuevo_data={'cantidad': 5})

    crear_cuentas_automaticamente_por_clientes()