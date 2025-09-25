import os
import subprocess
import re

# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("===========================================")
    print("        GESTOR DE COMMITS ESTIX         ")
    print("===========================================")
    print(f"{Colors.ENDC}")

def print_status(msg, color=Colors.OKCYAN):
    print(f"{color}{msg}{Colors.ENDC}")

def run_cmd(cmd, cwd=None, check_error=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print_status(f"⚠️ Error ejecutando: {cmd}", Colors.FAIL)
        print(result.stderr)  # mostrar el error de git en rojo
        if check_error:
            input("Presiona ENTER para salir...")  # detener cierre automático
            exit(1)
    return result.stdout.strip()

def input_with_confirm(prompt, color=Colors.OKBLUE, confirm_msg=None):
    while True:
        value = input(f"{color}{prompt}{Colors.ENDC}").strip()
        if confirm_msg:
            print(f"{Colors.WARNING}{confirm_msg}: {Colors.BOLD}{value}{Colors.ENDC}")
            confirm = input(f"{Colors.OKCYAN}¿Es correcto? (s/n): {Colors.ENDC}").strip().lower()
            if confirm == 's':
                return value
            else:
                print_status("Por favor, ingresa el valor nuevamente...", Colors.WARNING)
        else:
            return value

def main():
    print_banner()
    # Pedir ruta y confirmar
    while True:
        repo_path = input_with_confirm(
            "Ruta donde guardar el repositorio: ",
            Colors.OKBLUE,
            confirm_msg="Ruta seleccionada"
        )
        if os.path.isdir(repo_path) or not os.path.exists(repo_path):
            break
        else:
            print_status("La ruta ya existe y no es un directorio. Intenta de nuevo.", Colors.FAIL)

    # Pedir repo y confirmar
    while True:
        remote_url = input_with_confirm(
            "URL del repositorio remoto: ",
            Colors.OKBLUE,
            confirm_msg="Repo seleccionado"
        )
        print_status(f"Repo a usar: {remote_url}", Colors.OKCYAN)
        input(f"{Colors.OKGREEN}Presiona ENTER para continuar o Ctrl+C para cancelar...{Colors.ENDC}")
        # Validación simple de URL
        remote_url = remote_url.strip()
        if remote_url.startswith("http") and (
            "github.com" in remote_url or remote_url.endswith(".git")
        ):
            break
        else:
            print_status("La URL no parece válida. Intenta de nuevo.", Colors.FAIL)

    os.makedirs(repo_path, exist_ok=True)
    print_status(f"Directorio preparado: {repo_path}", Colors.OKGREEN)

    if not os.path.exists(os.path.join(repo_path, ".git")):
        print_status("Inicializando repositorio git...", Colors.OKCYAN)
        run_cmd("git init", cwd=repo_path)
        run_cmd(f"git remote add origin {remote_url}", cwd=repo_path)
        print_status("Repositorio git inicializado y remoto agregado.", Colors.OKGREEN)

    log = run_cmd("git log -1 --pretty=%B", cwd=repo_path, check_error=False)

    if not log:
        print_status("No hay commits previos. Creando commit inicial...", Colors.WARNING)
        with open(os.path.join(repo_path, "README.md"), "w", encoding="utf-8") as f:
            f.write("# SKYDROPX\n\nRepositorio inicializado automáticamente.\n")
        run_cmd("git add README.md", cwd=repo_path)
        run_cmd('git commit -m "INITIAL COMMIT"', cwd=repo_path)
        print_status("Commit inicial creado.", Colors.OKGREEN)

        # Subir al remoto
        run_cmd("git branch -M main", cwd=repo_path)
        run_cmd("git push -u origin main", cwd=repo_path)
        print_status("Commit inicial subido al remoto.", Colors.OKGREEN)
    else:
        # Crear commit automático
        match = re.search(r"UPDATE AUTO (\d+)", log)
        n = int(match.group(1)) + 1 if match else 1
        commit_msg = f"UPDATE AUTO {n}"

        run_cmd("git add .", cwd=repo_path)
        run_cmd(f'git commit -m "{commit_msg}"', cwd=repo_path)
        print_status(f"Commit creado: {commit_msg}", Colors.OKGREEN)

        # Push al remoto
        run_cmd("git push origin main", cwd=repo_path)
        print_status("Cambios subidos al remoto.", Colors.OKGREEN)

    input("\n✅ Proceso terminado. Presiona ENTER para salir...")

if __name__ == "__main__":
    main()
