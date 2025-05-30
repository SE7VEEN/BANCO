
import os
import json
import random
import sys


from cliente.cuentas.cuenta2 import Cuenta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from general.utils.utils import cargar_cuentas, guardar_cuentas



# BASE_DIR ahora apunta a la raíz del proyecto BANCO/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# CLIENTES_PATH apunta a BANCO/general/datos/clientes.json
CLIENTES_PATH = os.path.join(BASE_DIR, 'general', 'datos', 'clientes.json')


"""
Crea una nueva cuenta para un cliente dado su ID de usuario.
Verifica que el cliente exista antes de crear la cuenta y la guarda en el sistema.
"""
def crear_cuenta_para_cliente(id_usuario):
    if not os.path.exists(CLIENTES_PATH):
        return None

    with open(CLIENTES_PATH, 'r') as f:
        clientes = json.load(f)

    id_usuario = int(id_usuario)
    cliente = next((c for c in clientes if c['id_usuario'] == id_usuario), None)
    if not cliente:
        return None

    # Genera una nueva cuenta con saldo y adeudos aleatorios
    nueva_cuenta = Cuenta(
        id_usuario=id_usuario,
        saldo=round(random.uniform(500, 100000), 2),
        adeudos=round(random.uniform(0, 2000), 2)
    )
    
    cuentas = cargar_cuentas()
    cuentas.append(nueva_cuenta)
    guardar_cuentas(cuentas)

    return nueva_cuenta

"""
Devuelve una lista de cuentas asociadas a un ID de usuario específico.
Si el ID no es válido, retorna una lista vacía.
"""

def obtener_cuentas_por_usuario(id_usuario):
    try:
        id_usuario = int(id_usuario)
        cuentas = cargar_cuentas()
        return [c for c in cuentas if c.id_usuario == id_usuario]
    except ValueError:
        return []
    
    

"""
Gestiona acciones sobre cuentas: agregar, eliminar o modificar.
- 'agregar': Añade una nueva cuenta si no existe ya.
- 'eliminar': Borra una cuenta existente.
- 'modificar': Actualiza los atributos permitidos de una cuenta.
"""

def gestionar_cuenta(accion, cuenta=None, id_cuenta=None, nuevos_datos=None):
    try:
        cuentas = cargar_cuentas()
        cuentas_dict = {c.id_cuenta: c for c in cuentas}

        if accion == 'agregar':
            if not cuenta or not cuenta.id_usuario:
                return False
            if cuenta.id_cuenta in cuentas_dict:
                return False
            cuentas_dict[cuenta.id_cuenta] = cuenta

        elif accion == 'eliminar':
            if not id_cuenta or id_cuenta not in cuentas_dict:
                return False
            del cuentas_dict[id_cuenta]

        elif accion == 'modificar':
            if not id_cuenta or not nuevos_datos or id_cuenta not in cuentas_dict:
                return False
            cuenta = cuentas_dict[id_cuenta]
            for key, value in nuevos_datos.items():
                # No se permite modificar el ID de la cuenta ni el ID del usuario
                if hasattr(cuenta, key) and key not in ['id_cuenta', 'id_usuario']:
                    try:
                        if key in ['saldo', 'adeudos']:
                            value = float(value)
                        setattr(cuenta, key, value)
                    except Exception as e:
                        return False
        else:
            return False

        guardar_cuentas(list(cuentas_dict.values()))
        return True

    except Exception as e:
        return False


"""
Crea cuentas automáticamente para todos los clientes que aún no tienen una cuenta asociada.
Lee los clientes desde el archivo y verifica si ya tienen cuentas antes de crear una nueva.
"""
def crear_cuentas_automaticamente_por_clientes():
    if not os.path.exists(CLIENTES_PATH):
        return
    
    with open(CLIENTES_PATH, 'r') as f:
        clientes = json.load(f)

    for cliente in clientes:
        id_usuario = cliente["id_usuario"]
        cuentas_existentes = obtener_cuentas_por_usuario(id_usuario)
        if not cuentas_existentes:
            crear_cuenta_para_cliente(id_usuario)
        else:
            pass
            


"""
Agrega una nueva tarjeta a una cuenta existente.
"""            
def agregar_tarjeta_a_cuenta(id_cuenta):
    cuentas = cargar_cuentas()
    cuenta_dict = {c.id_cuenta: c for c in cuentas}

    if id_cuenta not in cuenta_dict:
        return False

    cuenta = cuenta_dict[id_cuenta]

    # Generamos una nueva tarjeta usando el método de Cuenta
    nueva_tarjeta = cuenta._generar_tarjetas(1)[0]
    cuenta.tarjetas.append(nueva_tarjeta)   

    # Actualizamos la cuenta usando gestionar_cuenta
    return gestionar_cuenta(
        accion="modificar",
        id_cuenta=id_cuenta,
        nuevos_datos={"tarjetas": cuenta.tarjetas}
    )
