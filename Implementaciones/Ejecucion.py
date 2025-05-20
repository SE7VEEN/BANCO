def iniciar_simulacion():
    solicitudes = generar_solicitudes_automaticas()
    for tipo, id_usuario, operacion in solicitudes:
        proceso = crear_proceso(tipo, id_usuario, operacion)
        prioridad = PRIORIDAD.get(proceso.tipo_cuenta or proceso.tipo_usuario, 1)
        cola_procesos.put((prioridad, time.time(), proceso))
        actualizar_estado_pcb(proceso.pid, "En espera")
    
    planificador()
