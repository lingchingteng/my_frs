import os
import shutil

from mtcnn_detect_faces import process_image


def test_process_image():
    path_image = "tests/testset/seven_people_image.jpg"

    # Clear output folder
    path_output_folder = "output/seven_people_image"

    if os.path.exists(path_output_folder):
        shutil.rmtree(path_output_folder)

    # process_image
    process_image(path_image)

    # check reuslts
    assert os.path.exists(path_output_folder)
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image.jpg"))
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_bbox.jpg"))
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_face_0.jpg"))
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_face_1.jpg"))
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_face_2.jpg"))
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_face_3.jpg"))
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_face_4.jpg"))
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_face_5.jpg"))
    assert os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_face_6.jpg"))
    assert not os.path.exists(
        os.path.join(path_output_folder, "seven_people_image_face_7.jpg"))

    if os.path.exists(path_output_folder):
        shutil.rmtree(path_output_folder)
