import os.path
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content into file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file that has to be read.",
            ),
            "file_content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            )
        },
    ),
)


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
