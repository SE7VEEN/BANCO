import json
import os
import random
from faker import Faker
from general.utils.utils import CLIENTES_PATH
from servidor.hilos.pcb import safe_json_read, safe_json_write
from general.utils.utils import quitar_acentos, formatear_telefono

fake = Faker('es_MX')

CAMPOS_MODIFICABLES = ["nombre", "contrasena", "num_telefono", "direccion"]

def generar_valor_aleatorio(campo):
    if campo == "nombre":
        return quitar_acentos(fake.name())
    elif campo == "contrasena":
        return fake.password(length=12, special_chars=True)
    elif campo == "num_telefono":
        return formatear_telefono(fake.phone_number())
    elif campo == "direccion":
        return quitar_acentos(fake.address().replace('\n', ', '))
    else:
        return None

def operacion_modificacion_datos(proceso):
    clientes = safe_json_read(CLIENTES_PATH, [])
    cliente_modificado = None

    for cliente in clientes:
        if cliente.get("id_usuario") == proceso.id_usuario:
            campo_a_modificar = random.choice(CAMPOS_MODIFICABLES)
            nuevo_valor = generar_valor_aleatorio(campo_a_modificar)

            cliente[campo_a_modificar] = nuevo_valor
            cliente_modificado = (campo_a_modificar, nuevo_valor)
            break

    if cliente_modificado:
        safe_json_write(CLIENTES_PATH, clientes)
        mensaje = f"Modificación exitosa: {campo_a_modificar} -> {nuevo_valor}"
        proceso.operacion = mensaje
    else:
        proceso.operacion = f"No se encontró al cliente con ID {proceso.id_usuario}"
