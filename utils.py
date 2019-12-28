import os
import shutil


def copy_input_to_database(path_input):
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    basename = os.path.basename(path_input)

    filename, ext = os.path.splitext(basename)

    path_output_folder = os.path.join(output_folder, filename)

    if not os.path.exists(path_output_folder):
        os.makedirs(path_output_folder)

    if os.path.exists(os.path.join(path_output_folder, basename)):
        return None

    shutil.copy2(path_input, path_output_folder)

    path_input = os.path.join(path_output_folder, basename)

    return path_input
