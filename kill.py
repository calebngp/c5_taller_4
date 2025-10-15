import os
import signal
import subprocess
import sys

def kill_process_by_pid(pid):
    """Termina un proceso por su PID"""
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Proceso {pid} terminado exitosamente")
        return True
    except ProcessLookupError:
        print(f"No se encontró el proceso con PID {pid}")
        return False
    except PermissionError:
        print(f"Sin permisos para terminar el proceso {pid}")
        return False
    except Exception as e:
        print(f"Error al terminar proceso {pid}: {e}")
        return False

def kill_process_by_name(process_name):
    """Termina procesos por nombre"""
    try:
        # Buscar procesos por nombre usando pgrep
        result = subprocess.run(['pgrep', '-f', process_name], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            killed_count = 0
            
            for pid in pids:
                if pid:  # Verificar que no esté vacío
                    if kill_process_by_pid(int(pid)):
                        killed_count += 1
            
            print(f"Se terminaron {killed_count} procesos con nombre '{process_name}'")
            return killed_count > 0
        else:
            print(f"No se encontraron procesos con nombre '{process_name}'")
            return False
            
    except Exception as e:
        print(f"Error al buscar procesos: {e}")
        return False

def force_kill_process(pid):
    """Fuerza la terminación de un proceso (SIGKILL)"""
    try:
        os.kill(pid, signal.SIGKILL)
        print(f"Proceso {pid} terminado forzosamente")
        return True
    except Exception as e:
        print(f"Error al forzar terminación del proceso {pid}: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python kill_process.py pid <PID>")
        print("  python kill_process.py name <NOMBRE_PROCESO>")
        print("  python kill_process.py force <PID>")
        return
    
    action = sys.argv[1]
    target = sys.argv[2]
    
    if action == "pid":
        try:
            pid = int(target)
            kill_process_by_pid(pid)
        except ValueError:
            print("PID debe ser un número")
    
    elif action == "name":
        kill_process_by_name(target)
    
    elif action == "force":
        try:
            pid = int(target)
            force_kill_process(pid)
        except ValueError:
            print("PID debe ser un número")
    
    else:
        print("Acción no válida. Use: pid, name, o force")

if __name__ == "__main__":
    main()