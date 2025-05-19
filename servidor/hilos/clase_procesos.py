from datetime import datetime
import os

class Proceso:
    def __init__(self, tipo_usuario, pid=None, ppid=None, estado="En espera", id_usuario=None, id_cuenta=None, tipo_cuenta=None, operacion=None):
        self.pid = pid or str(os.getpid())
        self.ppid = ppid or str(os.getppid())
        self.estado = estado
        self.id_cuenta = id_cuenta
        self.id_usuario = id_usuario
        self.tipo_usuario = tipo_usuario
        self.tipo_cuenta = tipo_cuenta
        self.operacion = operacion or "Ninguna"
        self.timestamp = datetime.now().strftime("%H:%M:%S")

    def to_dict(self):
        return {
            "PID": self.pid,
            "PPID": self.ppid,
            "Estado": self.estado,
            "IDUsuario": self.id_usuario,
            "IDCuenta": self.id_cuenta,
            "TipoUsuario": self.tipo_usuario,
            "TipoCuenta": self.tipo_cuenta,
            "Operacion": self.operacion,
            "Timestamp": self.timestamp
        }
