def despachar_proceso(proceso, semaforo):
    try:
        # FIFO ya lo controla el planificador
        actualizar_estado_pcb(proceso.pid, estado="En ejecución", operacion=f"Asignado a {proceso.destino}")

        # Ejecuta la operación
        if proceso.operacion == "Depósito":
            operacion_deposito(proceso, monto=100.0, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Consulta":
            operacion_consulta(proceso, cuentas_lock=cuentas_lock)
        else:
            actualizar_estado_pcb(proceso.pid, estado="Error", operacion="Operación no implementada")

    finally:
        semaforo.release()
