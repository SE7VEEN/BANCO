def asignar_prioridad(self):
    if self.tipo_usuario == "Cliente" and self.tipo_cuenta == "Premium":
        return 1  # Mayor prioridad
    return 2

def definir_destino(self):
    if self.operacion in ["Depósito", "Retiro", "Transferencia"]:
        return "Ventanilla"
    elif self.operacion in ["Consulta", "Simulación"]:
        return "Asesor"
    return "Desconocido"
