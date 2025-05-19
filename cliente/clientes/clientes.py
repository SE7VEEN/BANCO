import os
import json
import random
from faker import Faker
import sys

# Corregido: doble guion bajo en __file__ y cierre del paréntesis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from general.utils.utils import quitar_acentos, formatear_telefono

class Client:
    def __init__(self, id_usuario=None, nombre=None, contrasena=None, num_telefono=None, direccion=None):
        fake = Faker('es_MX')
        self.id_usuario = id_usuario or self._generar_id_unico()
        self.nombre = nombre or quitar_acentos(fake.name())
        self.contrasena = contrasena or self._generar_contrasena()
        self.num_telefono = num_telefono or formatear_telefono(fake.phone_number())
        self.direccion = direccion or quitar_acentos(fake.address().replace('\n', ', '))

    def _generar_id_unico(self):
        existentes = set()
        if os.path.exists('clientes.json'):
            with open('clientes.json', 'r') as f:
                clientes = json.load(f)
                existentes = {c['id_usuario'] for c in clientes}
        while True:
            nuevo_id = random.randint(1000, 9999)
            if nuevo_id not in existentes:
                return nuevo_id

    def _generar_contrasena(self):
        caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!^*'
        return ''.join(random.choice(caracteres) for _ in range(12))

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'contrasena': self.contrasena,
            'num_telefono': self.num_telefono,
            'direccion': self.direccion
        }
