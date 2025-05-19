import sys
import os
# Corregido: doble guion bajo en __file__ y cierre del paréntesis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from clientes.clientes import Client
from clientes.gestor import gestionar_clientes
from cuentas.gestion_cuenta import crear_cuentas_automaticamente_por_clientes

if __name__ == "__main__":
    cliente_aleatorio = Client()
    gestionar_clientes('agregar', cliente=cliente_aleatorio)
    gestionar_clientes('eliminar', id_usuario=9819)
    gestionar_clientes('generar', nuevo_data={'cantidad': 5})

    crear_cuentas_automaticamente_por_clientes()
