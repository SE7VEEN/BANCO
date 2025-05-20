import sys
import os
import json
import random
import time

from multiprocessing import Process
from general.utils.utils import inicializar_archivo, pcb_lock, cuentas_lock
from servidor.hilos.operaciones import ejecutar_operacion


def generar_solicitudes_automaticas():
    operaciones_clientes = ["Consulta de saldo", "Transferencia", "Depósito", "Retiro"]
    operaciones_visitantes = ["Consulta de servicios", "Creación de cuenta"]
    solicitudes = []

    with cuentas_lock:
        inicializar_archivo('cuentas.json')
        with open('cuentas.json', 'r') as f:
            cuentas = json.load(f)

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
            inicializar_archivo('pcb.json')
            with open('pcb.json', 'r') as f:
                procesos = json.load(f)

        print("\n=== MONITOR DE PROCESOS ===")
        print(f"Procesos totales: {len(procesos)}")
        for p in procesos[-5:]:
            print(f"PID: {p['PID']} | Estado: {p['Estado']} | Operación: {p['Operacion']}")
    except Exception as e:
        print(f"Error en monitor: {str(e)}")

if __name__ == "__main__":
    for f in ['pcb.json', 'clientes.json', 'cuentas.json']:
        inicializar_archivo(f)

    solicitudes = generar_solicitudes_automaticas()
    print("Solicitudes generadas:")
    for i, s in enumerate(solicitudes, 1):
        print(f"{i}. Tipo: {s[0]}, ID: {s[1]}, Operación: {s[2]}")

    procesos = []
    for args in solicitudes:
        p = Process(target=ejecutar_operacion, args=args)
        p.start()
        procesos.append(p)
        time.sleep(0.5)

    for p in procesos:
        p.join()

    monitor_procesos()
    print("\nSistema bancario: todas las operaciones completadas.")
