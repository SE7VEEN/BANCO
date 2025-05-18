from collections import deque

class Scheduler:
    def __init__(self):
        self.cola_fifo = deque()
    
    def agregar_proceso_fifo(self, pid):
        self.cola_fifo.append(pid)
    
    def siguiente_proceso_fifo(self):
        return self.cola_fifo.popleft() if self.cola_fifo else None

    def planificar_sjf(self, procesos):
        return sorted(procesos, key=lambda x: x["tiempo_estimado"])