def actualizar_estado_pcb(pid, nuevo_estado):
    with pcb_lock:
        with open(PCB_PATH, 'r+') as f:
            pcb = json.load(f)
            for p in pcb:
                if p["PID"] == pid:
                    p["Estado"] = nuevo_estado
                    p["Timestamp"] = datetime.now().strftime("%H:%M:%S")
                    break
            f.seek(0)
            json.dump(pcb, f, indent=4)
            f.truncate()
