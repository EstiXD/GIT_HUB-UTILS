import os
import subprocess
import re

# Ruta de la carpeta
repo_path = r"TU RUTA A GUARDAR HERE"

# URL de tu repo
remote_url = "TU RUTA DE REPO HERE"

# Función para ejecutar comandos
def run_cmd(cmd, cwd=None, check_error=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    if result.returncode != 0 and check_error:
        print(f"Error ejecutando: {cmd}\n{result.stderr}")
    return result.stdout.strip()

# Crear carpeta si no existe
os.makedirs(repo_path, exist_ok=True)

# Inicializar git si no existe
if not os.path.exists(os.path.join(repo_path, ".git")):
    run_cmd("git init", cwd=repo_path)
    run_cmd(f"git remote add origin {remote_url}", cwd=repo_path)

# Verificar si hay commits
log = run_cmd("git log -1 --pretty=%B", cwd=repo_path, check_error=False)

if not log:
    # Si no hay commits, crear un commit inicial
    with open(os.path.join(repo_path, "README.md"), "w", encoding="utf-8") as f:
        f.write("# ESTIX\n\nRepositorio inicializado automáticamente.\n")
    run_cmd("git add README.md", cwd=repo_path)
    run_cmd('git commit -m "INITIAL COMMIT"', cwd=repo_path)

# Ahora obtener último commit
log = run_cmd("git log -1 --pretty=%B", cwd=repo_path)

# Buscar número de UPDATE
match = re.search(r"UPDATE (\d+)", log)
if match:
    n = int(match.group(1)) + 1
else:
    n = 1

commit_msg = f"UPDATE AUTO {n}"

# Agregar cambios y hacer commit
run_cmd("git add -A", cwd=repo_path)
run_cmd(f'git commit -m "{commit_msg}" || echo "No changes to commit"', cwd=repo_path)

# Asegurar que la rama sea main antes del push
run_cmd("git branch -M main", cwd=repo_path)

# Push al repo
run_cmd("git push -u origin main --force", cwd=repo_path)

print(f"Commit realizado: {commit_msg}")
