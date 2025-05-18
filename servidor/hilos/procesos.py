import random
from time import sleep

class Proceso:
    def __init__(self, pid, ppid, cuenta, operacion, estado, tipo, prioridad=0):
        self.pid = pid           # ID del proceso
        self.ppid = ppid         # ID del proceso padre
        self.estado = estado     # "nuevo", "listo", "ejecutando", "bloqueado", "terminado"
        self.tipo = tipo         # "cliente", "visitante"
        self.cuenta = cuenta     # "Estandar", "Premium"
        self.prioridad = prioridad
        self.operacionActual = operacion  # En que operacion se encuentra el proceso
    
    def mostrar_info(self):
        print(f"Proceso ID: {self.pid}")
        print(f"Proceso Padre ID: {self.ppid}")
        print(f"Estado: {self.estado}")
        print(f"Tipo: {self.tipo}")
        print(f"Cuenta: {self.cuenta}")
        print(f"Prioridad: {self.prioridad}")
        print(f"Operación actual: {self.operacionActual}")
        print("-" * 30)

def generar_proceso_automatico(pid_counter):
    # Datos aleatorios para el proceso
    estados = ["nuevo", "listo", "ejecutando", "bloqueado", "terminado"]
    tipos = ["cliente", "visitante"]
    cuentas = ["Estandar", "Premium"]
    operaciones = ["Lectura", "Escritura", "Cálculo", "Consulta", "Actualización"]
    
    pid = f"P{pid_counter}"
    ppid = f"P{random.randint(0, pid_counter-1)}" if pid_counter > 0 else "0"
    cuenta = random.choice(cuentas)
    operacion = random.choice(operaciones)
    estado = random.choice(estados)
    tipo = random.choice(tipos)
    prioridad = random.randint(0, 5)
    
    return Proceso(pid, ppid, cuenta, operacion, estado, tipo, prioridad)

def crear_proceso_manual():
    print("\nCreando nuevo proceso...")
    pid = input("Ingrese el ID del proceso: ")
    ppid = input("Ingrese el ID del proceso padre: ")
    cuenta = input("Tipo de cuenta (Estandar/Premium): ").capitalize()
    operacion = input("Operación actual: ")
    estado = input("Estado (nuevo/listo/ejecutando/bloqueado/terminado): ").lower()
    tipo = input("Tipo (cliente/visitante): ").lower()
    prioridad = input("Prioridad (número, 0 por defecto): ")
    
    try:
        prioridad = int(prioridad) if prioridad else 0
    except ValueError:
        print("Prioridad no válida, se establecerá a 0")
        prioridad = 0
    
    return Proceso(pid, ppid, cuenta, operacion, estado, tipo, prioridad)

def mostrar_procesos(procesos):
    if not procesos:
        print("\nNo hay procesos registrados.")
    else:
        print("\nListado de procesos:")
        for proceso in procesos:
            proceso.mostrar_info()

def simular_procesos(procesos):
    if not procesos:
        print("No hay procesos para simular")
        return
    
    print("\nSimulando estados de procesos...")
    estados = ["listo", "ejecutando", "bloqueado", "terminado"]
    
    for proceso in procesos:
        if proceso.estado != "terminado":
            nuevo_estado = random.choice(estados)
            print(f"Proceso {proceso.pid} cambió de {proceso.estado} a {nuevo_estado}")
            proceso.estado = nuevo_estado
            sleep(0.5)  # Pequeña pausa para efecto de simulación

# Programa principal
if __name__ == "__main__":
    procesos = []
    pid_counter = 0
    
    while True:
        print("\nSistema de Gestión de Procesos")
        print("1. Crear proceso manual")
        print("2. Crear proceso automático")
        print("3. Crear múltiples procesos automáticos")
        print("4. Mostrar todos los procesos")
        print("5. Simular cambios de estado")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nuevo_proceso = crear_proceso_manual()
            procesos.append(nuevo_proceso)
            pid_counter += 1
            print("\nProceso creado exitosamente!")
        
        elif opcion == "2":
            nuevo_proceso = generar_proceso_automatico(pid_counter)
            procesos.append(nuevo_proceso)
            pid_counter += 1
            print("\nProceso automático creado:")
            nuevo_proceso.mostrar_info()
        
        elif opcion == "3":
            cantidad = input("¿Cuántos procesos desea crear? (default 5): ")
            try:
                cantidad = int(cantidad) if cantidad else 5
            except ValueError:
                cantidad = 5
            
            print(f"\nCreando {cantidad} procesos automáticos...")
            for _ in range(cantidad):
                nuevo_proceso = generar_proceso_automatico(pid_counter)
                procesos.append(nuevo_proceso)
                pid_counter += 1
                nuevo_proceso.mostrar_info()
                sleep(0.3)
        
        elif opcion == "4":
            mostrar_procesos(procesos)
        
        elif opcion == "5":
            simular_procesos(procesos)
        
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")