# GIT-UTILS

Este repositorio contiene dos scripts en Python para automatizar la inicialización, actualización y subida de cambios a un repositorio Git en GitHub.

## Archivos

### 1. GITHUB-UPDATE-INPUT.PY

Script interactivo que guía al usuario para:

- Seleccionar la ruta local donde se guardará el repositorio.
- Ingresar y confirmar la URL del repositorio remoto.
- Inicializar el repositorio local si no existe.
- Crear un commit inicial si es necesario.
- Realizar commits automáticos con mensajes incrementales (`UPDATE AUTO N`).
- Subir los cambios a la rama `main` del repositorio remoto.

**Uso:**
```bash
python GITHUB-UPDATE-INPUT.PY
```
Sigue las instrucciones en pantalla.

---

### 2. GITHUB-UPDATE-AUTO.PY

Script automático pensado para integraciones o tareas programadas. Realiza:

- Inicialización del repositorio si no existe.
- Commit inicial si es necesario.
- Commits automáticos con mensajes incrementales (`UPDATE AUTO N`).
- Push forzado a la rama `main`.

**Configuración:**
Edita las siguientes variables al inicio del archivo:
```python
repo_path = r"TU RUTA A GUARDAR HERE"
remote_url = "TU RUTA DE REPO HERE"
```

**Uso:**
```bash
python GITHUB-UPDATE-AUTO.PY
```

---

## Requisitos

- Python 3.x
- Git instalado y disponible en el PATH

## Notas

- Ambos scripts están pensados para usarse en entornos Windows, pero pueden adaptarse fácilmente a otros sistemas.
- El script automático sobrescribe la rama `main` en el remoto (`--force`).

---

## ⚠️ Advertencias

- **¡Cuidado!** El script `GITHUB-UPDATE-AUTO.PY` utiliza `git push --force`, lo que puede sobrescribir el historial remoto de la rama `main`. No lo uses en repositorios donde colaboran varias personas o donde no quieras perder historial.
- Antes de ejecutar cualquiera de los scripts, asegúrate de tener respaldo de tus archivos importantes.
- Verifica que las rutas y URLs proporcionadas sean correctas para evitar sobrescribir otros repositorios o carpetas.
- Usa estos scripts bajo tu propio riesgo. No nos hacemos responsables por pérdida de información.
