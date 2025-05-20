import os
import json
import random
import sys
import time
from multiprocessing import Process, Manager
from general.utils.utils import (inicializar_archivo, pcb_lock, cuentas_lock, 
                                CUENTAS_PATH, PCB_PATH, CLIENTES_PATH)

# Cambia esta importación para usar la implementación real
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from servidor.hilos.operaciones import ejecutar_operacion

def generar_solicitudes_automaticas():
    operaciones_clientes = ["Consulta de saldo", "Transferencia", "Depósito", "Retiro"]
    operaciones_visitantes = ["Consulta de servicios", "Creación de cuenta"]
    solicitudes = []

    with cuentas_lock:
        inicializar_archivo(CUENTAS_PATH)
        with open(CUENTAS_PATH, 'r') as f:
            try:
                cuentas = json.load(f)
            except json.JSONDecodeError:
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
                try:
                    procesos = json.load(f)
                except json.JSONDecodeError:
                    procesos = []

        print("\n=== MONITOR DE PROCESOS ===")
        print(f"Procesos totales: {len(procesos)}")
        for p in procesos[-5:]:
            print(f"PID: {p.get('PID')} | Operación: {p.get('Operacion')} | Estado: {p.get('Estado')}")
    except Exception as e:
        print(f"Error en monitor: {str(e)}")

if __name__ == "__main__":
    # Initialize all required files with proper paths
    for f in [PCB_PATH, CLIENTES_PATH, CUENTAS_PATH]:
        inicializar_archivo(f)

    solicitudes = generar_solicitudes_automaticas()
    print("Solicitudes generadas:")
    for i, s in enumerate(solicitudes, 1):
        print(f"{i}. Tipo: {s[0]}, ID: {s[1] or 'N/A'}, Operación: {s[2]}")

    # Usar Manager para compartir estado entre procesos
    with Manager() as manager:
        procesos = []
        for args in solicitudes:
            p = Process(target=ejecutar_operacion, args=args)
            p.start()
            procesos.append(p)
            time.sleep(0.2)  # Reducir el tiempo de espera entre procesos

        for p in procesos:
            p.join()

    monitor_procesos()
    print("\nSistema bancario: todas las operaciones completadas.")