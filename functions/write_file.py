import os.path

def write_file(working_directory, file_path, file_content):
    file = os.path.join(working_directory, file_path)
    if not os.path.abspath(file).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(file, "w") as fopen:
            fopen.write(file_content)
            return f'Successfully wrote to "{file_path}" ({len(file_content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

