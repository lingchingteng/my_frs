import glob
import os
from argparse import ArgumentParser

import cv2
from mtcnn.mtcnn import MTCNN

from utils import copy_input_to_database

detector = MTCNN()


def main(args):

    if os.path.isdir(args.path_input):
        path_images = sorted(
            glob.glob(os.path.join(args.path_input, "*.[j|J][p|P][g|G]")))

        for path_image in path_images:
            process_image(path_image)

    else:
        if is_support_file_type(args.path_input):
            process_image(args.path_input)


def is_support_file_type(path_image):

    support_file_types = ['.jpg', '.JPG']

    if os.path.splitext(path_image)[1] in support_file_types:
        return True

    return False


def process_image(path_raw_input):

    path_input = copy_input_to_database(path_raw_input)

    if not path_input:
        print("[Warning] "
              "There is already have same image filename in database (%s)" %
              (os.path.basename(path_raw_input)))
        return
    else:
        print("[Info] " "Processing (%s)..." % (os.path.basename(path_input)))

        dets = detect_faces_from_path(path_input)
        save_faces(path_input, dets)
        draw_bounding_box_and_save(path_input, dets)


def draw_bounding_box_and_save(path_image, dets):

    img = cv2.imread(path_image)

    for det in dets:

        line_width = min(
            int(min(img.shape[0:2]) * 0.01),  # Basic width, img too big
            int(min(det['box'][2], det['box'][3]) * 0.08),  # face too big
        )

        cv2.rectangle(
            img, (det['box'][0], det['box'][1]),
            (det['box'][0] + det['box'][2], det['box'][1] + det['box'][3]),
            (255, 0, 0), line_width)

    filename, ext = os.path.splitext(path_image)
    path_bbox_image = path_image.replace(ext, "_bbox%s" % (ext, ))

    cv2.imwrite(path_bbox_image, img)


def save_faces(path_image, dets):

    img = cv2.imread(path_image)

    for idx, det in enumerate(dets):
        bbox = det['box']

        cropped_face = img[
            max(0, bbox[1]):min(img.shape[0] - 1, bbox[1] + bbox[3]),
            max(0, bbox[0]):min(img.shape[1] - 1, bbox[0] + bbox[2])
        ]  # yapf: disable

        cropped_face = cv2.resize(cropped_face, (160, 160))

        filename, ext = os.path.splitext(path_image)
        path_face = path_image.replace(ext, "_face_%d%s" % (idx, ext))

        cv2.imwrite(path_face, cropped_face)


def detect_faces_from_path(image_path):
    img = cv2.imread(image_path)

    return detect_faces_from_image(img)


def detect_faces_from_image(img):

    dets = detector.detect_faces(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    return dets


if __name__ == "__main__":
    ap = ArgumentParser()

    ap.add_argument("path_input", help="Path of Input")

    args = ap.parse_args()

    main(args)
