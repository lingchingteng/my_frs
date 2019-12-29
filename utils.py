import os
import shutil
import re


def copy_input_to_database(path_input):

    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    basename = os.path.basename(path_input)

    filename, ext = os.path.splitext(basename)

    path_output_folder = os.path.join(output_folder, filename)

    if not os.path.exists(path_output_folder):
        os.makedirs(path_output_folder)
    else:
        print("Folder %s is already existed." % (path_output_folder))
        return None

    shutil.copy2(path_input, path_output_folder)

    path_input = os.path.join(path_output_folder, basename)

    return path_input


def is_support_file_type(path_image):

    re_support_file_types = ".(png|jpe?g)"

    if re.match(re_support_file_types,
                os.path.splitext(path_image)[1].lower()):
        return True

    return False
