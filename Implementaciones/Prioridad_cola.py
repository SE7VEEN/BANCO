from queue import PriorityQueue
from threading import Semaphore, Lock, Thread

# 0 = más prioritario
PRIORIDAD = {
    "Premium": 0,
    "Estándar": 1,
    "Visitante": 1,
}

cola_procesos = PriorityQueue()
mutex_cola = Lock()
