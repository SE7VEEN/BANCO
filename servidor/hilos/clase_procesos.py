from datetime import *
import os

class Proceso:
    def __init__(self, tipo_usuario, id_usuario=None, id_cuenta=None, tipo_cuenta=None, operacion=None):
        self.pid = os.getpid()
        self.tipo_usuario = tipo_usuario
        self.id_usuario = id_usuario
        self.id_cuenta = id_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.operacion = operacion
        self.estado = "En ejecución"
        self.tiempo_inicio = time.time()
        self.tiempo_fin = None

    def to_dict(self):
        return {
            "PID": self.pid,
            "TipoUsuario": self.tipo_usuario,
            "IDUsuario": self.id_usuario,
            "IDCuenta": self.id_cuenta,
            "TipoCuenta": self.tipo_cuenta,
            "Operacion": self.operacion,
            "Estado": self.estado,
            "TiempoInicio": self.tiempo_inicio,
            "TiempoFin": self.tiempo_fin
        }
