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

def print_status(msg, color=Colors.OKCYAN):
    print(f"{color}{msg}{Colors.ENDC}")

def print_banner():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("===========================================")
    print("      GITHUB UPDATE AUTO ESTIX             ")
    print("===========================================")
    print(f"{Colors.ENDC}")

# Ruta de la carpeta
repo_path = r"C:\SCRIPS\SKYDROPX-main"

# URL de tu repo
remote_url = "https://github.com/EstiXD/SKYDROPX"

# Función para ejecutar comandos
def run_cmd(cmd, cwd=None, check_error=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    if result.returncode != 0 and check_error:
        print_status(f"⚠️ Error ejecutando: {cmd}", Colors.FAIL)
        print(f"{Colors.FAIL}{result.stderr}{Colors.ENDC}")
    return result.stdout.strip()

def main():
    print_banner()
    print_status(f"Directorio de trabajo: {repo_path}", Colors.OKBLUE)
    print_status(f"Repositorio remoto: {remote_url}", Colors.OKBLUE)
    print(f"{Colors.OKCYAN}{'-'*40}{Colors.ENDC}")

    # Crear carpeta si no existe
    os.makedirs(repo_path, exist_ok=True)

    # Inicializar git si no existe
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print_status("Inicializando repositorio git...", Colors.OKCYAN)
        run_cmd("git init", cwd=repo_path)
        run_cmd(f"git remote add origin {remote_url}", cwd=repo_path)
        print_status("Repositorio git inicializado y remoto agregado.", Colors.OKGREEN)

    # Verificar si hay commits
    log = run_cmd("git log -1 --pretty=%B", cwd=repo_path, check_error=False)

    if not log:
        print_status("No hay commits previos. Creando commit inicial...", Colors.WARNING)
        with open(os.path.join(repo_path, "README.md"), "w", encoding="utf-8") as f:
            f.write("# ESTIX\n\nRepositorio inicializado automáticamente.\n")
        run_cmd("git add README.md", cwd=repo_path)
        run_cmd('git commit -m "INITIAL COMMIT"', cwd=repo_path)
        print_status("Commit inicial creado.", Colors.OKGREEN)

    # Ahora obtener último commit
    log = run_cmd("git log -1 --pretty=%B", cwd=repo_path)

    # Buscar número de UPDATE
    match = re.search(r"UPDATE (\d+)", log)
    if match:
        n = int(match.group(1)) + 1
    else:
        n = 1

    commit_msg = f"UPDATE AUTO {n}"

    print_status("Agregando cambios...", Colors.OKCYAN)
    run_cmd("git add -A", cwd=repo_path)
    print_status(f"Realizando commit: {commit_msg}", Colors.OKCYAN)
    run_cmd(f'git commit -m "{commit_msg}" || echo "No changes to commit"', cwd=repo_path)

    print_status("Asegurando rama main...", Colors.OKCYAN)
    run_cmd("git branch -M main", cwd=repo_path)

    print_status("Subiendo cambios al remoto...", Colors.OKCYAN)
    run_cmd("git push -u origin main --force", cwd=repo_path)

    print(f"{Colors.OKGREEN}✅ Commit realizado: {commit_msg}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'-'*40}{Colors.ENDC}")

if __name__ == "__main__":
    main()
