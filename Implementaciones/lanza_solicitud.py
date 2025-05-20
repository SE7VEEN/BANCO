import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from servidor.hilos.operaciones import generar_solicitudes_automaticas, ejecutar_operacion
from multiprocessing import Process

def lanzar_solicitudes():
    solicitudes = generar_solicitudes_automaticas()
    procesos = []
    for tipo, id_usuario, operacion in solicitudes:
        p = Process(target=ejecutar_operacion, args=(tipo, id_usuario, operacion))
        p.start()
        procesos.append(p)
    for p in procesos:
        p.join()

    return solicitudes