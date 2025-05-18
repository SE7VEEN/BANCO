import json
import os
from pathlib import Path

class PCBManager:
    def __init__(self):
        self.pcb = []
        self.db_path = Path(__file__).parent / "database.json"
        self._inicializar_db()

    def _inicializar_db(self):
        """Crea el archivo JSON si no existe con la estructura básica"""
        if not self.db_path.exists():
            estructura_inicial = {
                "clientes": [],
                "visitantes": [],
                "cola_fifo": [],
                "pcb": []
            }
            with open(self.db_path, 'w') as f:
                json.dump(estructura_inicial, f, indent=4)

    def _cargar_db(self):
        """Carga los datos del archivo JSON"""
        with open(self.db_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Si el archivo está corrupto, lo reiniciamos
                self._inicializar_db()
                return self._cargar_db()

    def crear_proceso(self, pid, ppid, tipo, estado="en_espera"):
        proceso = {
            "PID": pid,
            "PPID": ppid,
            "Tipo": tipo,
            "Estado": estado,
            "Registro": "cliente" if tipo != "visitante" else "no_registrado"
        }
        self.pcb.append(proceso)
        self._actualizar_json()
    
    def cambiar_estado(self, pid, nuevo_estado):
        for proceso in self.pcb:
            if proceso["PID"] == pid:
                proceso["Estado"] = nuevo_estado
        self._actualizar_json()
    
    def _actualizar_json(self):
        """Actualiza el archivo JSON con los datos actuales"""
        data = self._cargar_db()
        data["pcb"] = self.pcb
        
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=4)