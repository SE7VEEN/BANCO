from server import BancoServer

def main():
    server = BancoServer()
    pid = 1001  # Simular PID único
    
    # Autenticación
    tipo = input("¿Cliente (C) o visitante (V)? ").upper()
    if tipo == "C":
        user = input("Usuario: ")
        password = input("Contraseña: ")
        server.pcb_manager.crear_proceso(pid, 0, "cliente")
    else:
        server.pcb_manager.crear_proceso(pid, 0, "visitante")
    
    # Agregar a cola FIFO
    server.scheduler.agregar_proceso_fifo(pid)
    
    # Simular operación
    server.atender_cliente(pid, "CONSULTA_SALDO")

if __name__ == "__main__":
    main()