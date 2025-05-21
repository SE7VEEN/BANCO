# prioridad2.py

def asignar_prioridad(tipo_usuario, tipo_cuenta):
    if tipo_usuario == "Cliente" and tipo_cuenta == "Premium":
        return 1  # Mayor prioridad
    return 2

def definir_destino(operacion):
    if operacion in ["Deposito", "Retiro", "Transferencia"]:
        return "Ventanilla"
    elif operacion in ["Consulta", "Simulación"]:
        return "Asesor"
    return "Desconocido"
