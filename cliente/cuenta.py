import json
import os

class Cuenta:
    def __init__(self, id_usuario, id_cuenta="", estado_cuenta="", tipo_cuenta="", tarjetas=None, saldo=True, adeudos="0"):
        self.id_usuario = id_usuario
        self.id_cuenta = id_cuenta
        self.estado_cuenta = estado_cuenta 
        self.tipo_cuenta = tipo_cuenta
        self.tarjetas = tarjetas if tarjetas is not None else []
        self.saldo = saldo
        self.adeudos = adeudos

    def to_dict(self):
        return {
            'id_usuario' : self.id_usuario,
            'id_cuenta': self.id_cuenta,
            'estado_cuenta': self.estado_cuenta,
            'tipo_cuenta': self.tipo_cuenta,
            'tarjetas': self.tarjetas,
            'saldo': self.saldo,
            'adeudos': self.adeudos
        }

def cargar_cuentas():
    """Carga las cuentas desde el archivo JSON"""
    if os.path.exists('cuentas.json'):
        with open('cuentas.json', 'r') as f:
            return json.load(f)
    return []

def guardar_cuentas(cuentas):
    """Guarda las cuentas en el archivo JSON"""
    with open('cuentas.json', 'w') as f:
        json.dump(cuentas, f, indent=4)

def generar_cuentas_desde_clientes():
    """Genera cuentas basadas en clientes existentes"""
    try:
        # Verificar existencia de clientes.json
        if not os.path.exists('clientes.json'):
            print("Error: No existe el archivo clientes.json")
            return False

        # Cargar datos
        with open('clientes.json', 'r') as f:
            clientes = json.load(f)
        
        cuentas = cargar_cuentas()
        cuentas_existentes = {c['id_cuenta']: c for c in cuentas}

        # Procesar clientes
        for cliente in clientes:
            id_cuenta = cliente['id_cuenta']
            
            if id_cuenta not in cuentas_existentes:
                nueva_cuenta = Cuenta(
                    id_cuenta=id_cuenta,
                    tarjetas=cliente.get('tarjetas', [])
                )
                cuentas.append(nueva_cuenta.to_dict())
                print(f"Cuenta creada para ID {id_cuenta}")

        guardar_cuentas(cuentas)
        print("Generación de cuentas completada.")
        return True
        
    except Exception as e:
        print(f"Error al generar cuentas: {str(e)}")
        return False

def gestionar_cuenta(accion, cuenta=None, id_cuenta=None, nuevos_datos=None):
    """
    Gestiona cuentas con las siguientes acciones:
    - 'agregar': Agrega una nueva cuenta
    - 'eliminar': Elimina una cuenta existente
    - 'modificar': Actualiza datos de una cuenta (excepto ID)
    """
    try:
        cuentas = cargar_cuentas()
        cuentas_dict = {c['id_cuenta']: c for c in cuentas}

        if accion == 'agregar':
            if not cuenta:
                print("Error: Se requiere objeto Cuenta para agregar")
                return False
                
            if cuenta.id_cuenta in cuentas_dict:
                print(f"Error: La cuenta {cuenta.id_cuenta} ya existe")
                return False
                
            cuentas_dict[cuenta.id_cuenta] = cuenta.to_dict()
            print(f"Cuenta {cuenta.id_cuenta} agregada correctamente")

        elif accion == 'eliminar':
            if not id_cuenta:
                print("Error: Se requiere id_cuenta para eliminar")
                return False
                
            if id_cuenta not in cuentas_dict:
                print(f"Error: La cuenta {id_cuenta} no existe")
                return False
                
            del cuentas_dict[id_cuenta]
            print(f"Cuenta {id_cuenta} eliminada correctamente")

        elif accion == 'modificar':
            if not id_cuenta or not nuevos_datos:
                print("Error: Se requiere id_cuenta y nuevos_datos para modificar")
                return False
                
            if id_cuenta not in cuentas_dict:
                print(f"Error: La cuenta {id_cuenta} no existe")
                return False
                
            # Validar que no se intente modificar el ID
            if 'id_cuenta' in nuevos_datos:
                print("Error: No se puede modificar el ID de la cuenta")
                return False
                
            # Actualizar solo campos permitidos
            for key, value in nuevos_datos.items():
                if key in cuentas_dict[id_cuenta] and key != 'id_cuenta':
                    cuentas_dict[id_cuenta][key] = value
                    
            print(f"Cuenta {id_cuenta} modificada correctamente")

        else:
            print("Error: Acción no válida. Use 'agregar', 'eliminar' o 'modificar'")
            return False
            
        guardar_cuentas(list(cuentas_dict.values()))
        return True
        
    except Exception as e:
        print(f"Error al gestionar cuenta: {str(e)}")
        return False
