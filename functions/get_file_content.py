import os.path

def get_file_content(working_directory, file_path):
    file = os.path.join(working_directory, file_path)
    abs_working_directory = os.path.abspath(working_directory)

    if not os.path.abspath(file).startswith(abs_working_directory):
        return f'Error: Cannot list "{file}" as it is outside the permitted working directory'

    if os.path.isfile(file) == False:
        return (f'Error: File not found or is not a regular file: "{file_path}"')

    MAX_CHARS = 10000
    try:
        with open(file, 'r') as f:
            file_content_string = f.read(MAX_CHARS)

        if os.path.getsize(file) > MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception:
        return (f'Error: Cannot read file "{file}"')


    return file_content_string