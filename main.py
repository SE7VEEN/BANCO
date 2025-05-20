import os
import json
import random
import sys
import time
from multiprocessing import Process, Manager, Lock

from general.utils.utils import (
    inicializar_archivo, pcb_lock, cuentas_lock,
    CUENTAS_PATH, PCB_PATH, CLIENTES_PATH
)

# Ajustar sys.path para importar correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from servidor.hilos.operaciones import ejecutar_operacion


def generar_solicitudes_automaticas():
    operaciones_clientes = ["Consulta de saldo", "Transferencia", "Depósito", "Retiro"]
    operaciones_visitantes = ["Consulta de servicios", "Creación de cuenta"]
    solicitudes = []

    with cuentas_lock:
        inicializar_archivo(CUENTAS_PATH)
        try:
            with open(CUENTAS_PATH, 'r') as f:
                cuentas = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            cuentas = []

    for cuenta in cuentas:
        id_usuario = cuenta.get('id_usuario')
        if id_usuario:
            for _ in range(random.randint(1, 3)):
                operacion = random.choice(operaciones_clientes)
                solicitudes.append(("Cliente", id_usuario, operacion))

    for _ in range(random.randint(2, 5)):
        operacion = random.choice(operaciones_visitantes)
        solicitudes.append(("Visitante", None, operacion))

    return solicitudes


def monitor_procesos():
    try:
        with pcb_lock:
            inicializar_archivo(PCB_PATH)
            with open(PCB_PATH, 'r') as f:
                procesos = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        procesos = []

    print("\n=== MONITOR DE PROCESOS ===")
    print(f"Procesos totales: {len(procesos)}")
    for p in procesos[-5:]:
        print(f"PID: {p.get('PID')} | Operación: {p.get('Operacion')} | Estado: {p.get('Estado')}")


if __name__ == "__main__":
    # Inicializar archivos necesarios
    for ruta in [PCB_PATH, CLIENTES_PATH, CUENTAS_PATH]:
        inicializar_archivo(ruta)

    # Generar solicitudes de operación
    solicitudes = generar_solicitudes_automaticas()
    print("Solicitudes generadas:")
    for i, (tipo, id_, operacion) in enumerate(solicitudes, 1):
        print(f"{i}. Tipo: {tipo}, ID: {id_ or 'N/A'}, Operación: {operacion}")

    # Ejecutar operaciones usando multiprocessing
    with Manager() as manager:
        shared_lock = Lock()
        procesos = []
        for args in solicitudes:
            # Si `ejecutar_operacion` acepta el lock como cuarto argumento, descomenta la línea siguiente:
            # p = Process(target=ejecutar_operacion, args=(*args, shared_lock))

            # Si no se necesita pasar el lock, usa esta:
            p = Process(target=ejecutar_operacion, args=args)

            p.start()
            procesos.append(p)
            time.sleep(0.2)  # Simula procesamiento escalonado

        for p in procesos:
            p.join()

    # Mostrar resumen de procesos
    monitor_procesos()
    print("\nSistema bancario: todas las operaciones completadas.")
