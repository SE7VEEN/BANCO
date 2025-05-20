def planificador():
    while not cola_procesos.empty():
        _, _, proceso = cola_procesos.get()
        actualizar_estado_pcb(proceso.pid, "En cola")

        if proceso.operacion in ["Consulta saldo", "Transferencia"]:
            atender_en_ventanilla(proceso)
        else:
            atender_con_asesor(proceso)
