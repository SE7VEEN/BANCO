import threading
import json
from pcb_manager import PCBManager
from scheduler import Scheduler

class BancoServer:
    def __init__(self):
        self.pcb_manager = PCBManager()
        self.scheduler = Scheduler()
        self.mutex = threading.Lock()
    
    def atender_cliente(self, pid, operacion):
        with self.mutex:  # Sincronización con Mutex
            self.pcb_manager.cambiar_estado(pid, "en_ejecucion")
            # Simular operación bancaria
            print(f"Ejecutando {operacion} para PID {pid}")
            self.pcb_manager.cambiar_estado(pid, "finalizado")