import uuid
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

"""
Clase que representa una cuenta bancaria.
Incluye generación automática de ID, tipo de cuenta, tarjetas y manejo de saldo y adeudos.
"""

class Cuenta:
    def __init__(self, id_cuenta="", id_usuario=None, estado_cuenta="activa", tipo_cuenta=None, 
                 tarjetas=None, saldo=0.0, adeudos=0.0):
        self.id_cuenta = id_cuenta or self._generar_id_cuenta()
        self.id_usuario = int(id_usuario) if id_usuario is not None else None
        self.estado_cuenta = estado_cuenta
        self.tipo_cuenta = tipo_cuenta or random.choices(
            ["estandar", "premium"], weights=[70, 30], k=1  # Probabilidad del 70% para "estandar", 30% para "premium"
        )[0]
        self.tarjetas = tarjetas if tarjetas is not None else self._generar_tarjetas()
        self.saldo = float(saldo)
        self.adeudos = float(adeudos)


    """
    Genera un identificador único para la cuenta con prefijo 'CTA-'
    seguido de los primeros 8 caracteres del UUID generado.
    """
    
    def _generar_id_cuenta(self):
        return f"CTA-{uuid.uuid4().hex[:8].upper()}"
    
    """
    Genera una o más tarjetas con formato de 16 dígitos divididos en bloques de 4
    y un código CVV de 3 dígitos. Por defecto genera una tarjeta.
    """

    def _generar_tarjetas(self, cantidad=1):
        tarjetas = []
        for _ in range(cantidad):
            numero = '-'.join([''.join(str(random.randint(0, 9)) for _ in range(4)) for _ in range(4)])
            cvv = ''.join(str(random.randint(0, 9)) for _ in range(3))
            tarjetas.append({'VISA': numero, 'cvv': cvv})
        return tarjetas

    """
    Convierte el objeto Cuenta a un diccionario para facilitar
    su serialización a JSON.
    """
    
    def to_dict(self):
        return {
            'id_cuenta': self.id_cuenta,
            'id_usuario': self.id_usuario,
            'estado_cuenta': self.estado_cuenta,
            'tipo_cuenta': self.tipo_cuenta,
            'tarjetas': self.tarjetas,
            'saldo': self.saldo,
            'adeudos': self.adeudos
        }


    """
    Crea una instancia de Cuenta a partir de un diccionario.
    """
    @classmethod
    def from_dict(cls, data):
        return cls(
            id_cuenta=data['id_cuenta'],
            id_usuario=data['id_usuario'],
            estado_cuenta=data.get('estado_cuenta', 'activa'),
            tipo_cuenta=data.get('tipo_cuenta'),
            tarjetas=data.get('tarjetas', []),
            saldo=data.get('saldo', 0.0),
            adeudos=data.get('adeudos', 0.0)
        )
