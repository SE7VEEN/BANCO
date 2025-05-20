with asesor_semaphore:
    actualizar_estado_pcb(pid, estado="Atendido por asesor", operacion="Simulación de cuenta")
    time.sleep(2)
    actualizar_estado_pcb(pid, estado="Finalizado", operacion="Simulación finalizada")
