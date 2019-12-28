import os
import shutil
from argparse import ArgumentParser

import cv2
from mtcnn.mtcnn import MTCNN

detector = MTCNN()


def copy_input_to_database(path_input):
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    basename = os.path.basename(path_input)
    filename, ext = os.path.splitext(basename)
    path_output_folder = os.path.join(output_folder, filename)
    if not os.path.exists(path_output_folder):
        os.makedirs(path_output_folder)

    shutil.copy2(path_input, path_output_folder)

    path_input = os.path.join(path_output_folder, basename)

    return path_input


def main(args):

    if ".mp4" == os.path.splitext(args.path_input)[1]:
        path_input = copy_input_to_database(args.path_input)

        detect_video(path_input)

    elif ".jpg" == os.path.splitext(args.path_input)[1]:

        path_input = copy_input_to_database(args.path_input)

        img = cv2.imread(path_input)

        detect_image(img, path_input, save_bbox=True, save_face=True)


def detect_video(path_video):

    cap = cv2.VideoCapture(path_video)

    frame_cnt = 0
    while cap.isOpened():

        ok, frame = cap.read()

        if not ok:
            cap.release()
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        dets = detect_image(frame)

        for idx, det in enumerate(dets):

            ext = os.path.splitext(path_video)[1]
            path_face = path_video.replace(
                ext, "frame_%d_face_%d" % (
                    frame_cnt,
                    idx,
                ) + ".jpg")

            cv2.imwrite(
                path_face,
                cv2.cvtColor(det['image_cropped_face'], cv2.COLOR_RGB2BGR))

        frame_cnt += 1


def detect_image(img, path_image, save_face=False, save_bbox=False):

    if path_image and save_bbox:
        bbox_img = img.copy()

    dets = detector.detect_faces(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    for idx, det in enumerate(dets):
        bbox = det['box']

        cropped_face = img[max(0, bbox[1]):min(img.shape[0] - 1, bbox[1] +
                                               bbox[3]),
                           max(0, bbox[0]):min(img.shape[1] - 1, bbox[0] +
                                               bbox[2])]
        cropped_face = cv2.resize(cropped_face, (160, 160))

        det['image_cropped_face'] = cropped_face

        if path_image and save_face:
            ext = os.path.splitext(path_image)[1]
            path_face = path_image.replace(ext, "_face_%d" % (idx, ) + ext)

            det['path_cropped_face'] = path_face

            cv2.imwrite(path_face, cropped_face)

        if path_image and save_bbox:
            line_width = min(
                int(min(img.shape[0:2]) * 0.01),  # Basic width, img too big
                int(min(det['box'][2], det['box'][3]) * 0.08),  # face too big
            )
            cv2.rectangle(
                bbox_img, (det['box'][0], det['box'][1]),
                (det['box'][0] + det['box'][2], det['box'][1] + det['box'][3]),
                (255, 0, 0), line_width)

    if path_image and save_bbox:
        filename, ext = os.path.splitext(path_image)
        path_face = path_image.replace(ext, "_detect.jpg")

        cv2.imwrite(path_face, bbox_img)

    return dets


if __name__ == "__main__":
    ap = ArgumentParser()

    ap.add_argument("path_input", help="Path of Input")

    args = ap.parse_args()

    main(args)
