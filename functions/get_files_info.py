import os.path

def get_files_info(working_directory, directory="."):
    dir = os.path.join(working_directory, directory)
    abs_working_directory = os.path.abspath(working_directory)

    if not os.path.abspath(dir).startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(dir) == False:
        return (f"Error: {dir} is not a directory")

    dir_list = ""
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        dir_list += f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir( file_path)}\n"

    return dir_list