semaforo_ventanillas = Semaphore(2)  # 2 ventanillas disponibles
semaforo_asesores = Semaphore(1)     # 1 asesor disponible

def atender_en_ventanilla(proceso):
    with semaforo_ventanillas:
        actualizar_estado_pcb(proceso.pid, "Atendiendo en ventanilla")
        time.sleep(2)
        actualizar_estado_pcb(proceso.pid, "Finalizado")

def atender_con_asesor(proceso):
    with semaforo_asesores:
        actualizar_estado_pcb(proceso.pid, "Atendiendo con asesor")
        time.sleep(3)
        actualizar_estado_pcb(proceso.pid, "Finalizado")
