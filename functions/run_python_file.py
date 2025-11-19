import os.path
import subprocess


def run_python_file(working_directory, file_path, args = []):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath( os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(abs_file_path) == False:
        return f'Error: File "{file_path}" not found.'
    if file_path.endswith('.py') == False:
        return f'Error: "{file_path}" is not a Python file.'
    try:
        output = []
        result = subprocess.run(
            ["python3", file_path, *args],
            cwd=abs_working_directory,
            capture_output=True,text=True,timeout=30)
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDOUT:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"