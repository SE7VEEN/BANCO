import json
import os
import uuid
import random

class Cuenta:
    def __init__(self, id_cuenta="", id_usuario=None, estado_cuenta="activa", tipo_cuenta="estándar", 
                 tarjetas=None, saldo=0.0, adeudos=0.0):
        self.id_cuenta = id_cuenta or self._generar_id_cuenta()
        self.id_usuario = int(id_usuario) if id_usuario is not None else None
        self.estado_cuenta = estado_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.tarjetas = tarjetas if tarjetas is not None else []
        self.saldo = float(saldo)
        self.adeudos = float(adeudos)

    def _generar_id_cuenta(self):
        return f"CTA-{uuid.uuid4().hex[:8].upper()}"

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

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_cuenta=data['id_cuenta'],
            id_usuario=data['id_usuario'],
            estado_cuenta=data.get('estado_cuenta', 'activa'),
            tipo_cuenta=data.get('tipo_cuenta', 'estándar'),
            tarjetas=data.get('tarjetas', []),
            saldo=data.get('saldo', 0.0),
            adeudos=data.get('adeudos', 0.0)
        )

def cargar_cuentas():
    if os.path.exists('cuentas.json'):
        with open('cuentas.json', 'r') as f:
            try:
                return [Cuenta.from_dict(c) for c in json.load(f)]
            except json.JSONDecodeError:
                return []
    return []

def guardar_cuentas(cuentas):
    with open('cuentas.json', 'w') as f:
        json.dump([c.to_dict() for c in cuentas], f, indent=4)

def crear_cuenta_para_cliente(id_usuario, tipo_cuenta="estándar"):
    try:
        if not os.path.exists('clientes.json'):
            print("Error: No existe el archivo de clientes")
            return None

        with open('clientes.json', 'r') as f:
            clientes = json.load(f)

        id_usuario = int(id_usuario)

        cliente = next((c for c in clientes if c['id_usuario'] == id_usuario), None)
        if not cliente:
            print(f"Error: No existe cliente con ID {id_usuario}")
            return None

        tarjetas = cliente.get("tarjetas", [])
        nueva_cuenta = Cuenta(
            id_usuario=id_usuario,
            tipo_cuenta=tipo_cuenta,
            tarjetas=tarjetas,
            saldo=round(random.uniform(500, 5000), 2),
            adeudos=round(random.uniform(0, 500), 2)
        )
        
        cuentas = cargar_cuentas()
        cuentas.append(nueva_cuenta)
        guardar_cuentas(cuentas)

        print(f"Cuenta {nueva_cuenta.id_cuenta} creada para cliente {id_usuario}")
        return nueva_cuenta

    except Exception as e:
        print(f"Error al crear cuenta: {str(e)}")
        return None

def obtener_cuentas_por_usuario(id_usuario):
    try:
        id_usuario = int(id_usuario)
        cuentas = cargar_cuentas()
        return [c for c in cuentas if c.id_usuario == id_usuario]
    except ValueError:
        print(f"Error: ID de usuario inválido {id_usuario}")
        return []

def gestionar_cuenta(accion, cuenta=None, id_cuenta=None, nuevos_datos=None):
    try:
        cuentas = cargar_cuentas()
        cuentas_dict = {c.id_cuenta: c for c in cuentas}

        if accion == 'agregar':
            if not cuenta or not cuenta.id_usuario:
                print("Error: Falta información para agregar la cuenta")
                return False
            if cuenta.id_cuenta in cuentas_dict:
                print(f"Error: La cuenta {cuenta.id_cuenta} ya existe")
                return False
            cuentas_dict[cuenta.id_cuenta] = cuenta
            print(f"Cuenta {cuenta.id_cuenta} agregada correctamente")

        elif accion == 'eliminar':
            if not id_cuenta or id_cuenta not in cuentas_dict:
                print("Error: Cuenta no encontrada para eliminar")
                return False
            del cuentas_dict[id_cuenta]
            print(f"Cuenta {id_cuenta} eliminada correctamente")

        elif accion == 'modificar':
            if not id_cuenta or not nuevos_datos or id_cuenta not in cuentas_dict:
                print("Error: Datos inválidos para modificar")
                return False
            cuenta = cuentas_dict[id_cuenta]
            for key, value in nuevos_datos.items():
                if hasattr(cuenta, key) and key not in ['id_cuenta', 'id_usuario']:
                    try:
                        if key in ['saldo', 'adeudos']:
                            value = float(value)
                        setattr(cuenta, key, value)
                    except Exception as e:
                        print(f"Error al actualizar {key}: {str(e)}")
                        return False
            print(f"Cuenta {id_cuenta} modificada correctamente")
        else:
            print("Error: Acción no válida")
            return False

        guardar_cuentas(list(cuentas_dict.values()))
        return True

    except Exception as e:
        print(f"Error al gestionar cuenta: {str(e)}")
        return False

def crear_cuentas_automaticamente_por_clientes():
    if not os.path.exists('clientes.json'):
        print("Error: No existe el archivo de clientes")
        return
    with open('clientes.json', 'r') as f:
        clientes = json.load(f)

    for cliente in clientes:
        crear_cuenta_para_cliente(cliente["id_usuario"], tipo_cuenta=random.choice(["estándar", "premium"]))

# Ejecutar si se llama directamente
if __name__ == "__main__":
    crear_cuentas_automaticamente_por_clientes()
#