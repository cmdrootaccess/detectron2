"""
Script that visualises and saves densepose results generated by apply_net.py in dump mode.
Only visualises for the largest person (largest bounding box) in the image.
"""

import sys
import pickle
import argparse
import numpy as np
import cv2

from densepose.structures import DensePoseResult
sys.path.append("/data/cvfs/as2562/detectron2/projects/DensePose/")
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def visualise_denspose_results(dump_file):
    with open(dump_file, 'rb') as f_results:
        data = pickle.load(f_results)

    # Loop through frames
    for entry in data:
        frame_fname = entry['file_name']
        print(frame_fname)
        frame = cv2.imread(frame_fname)
        orig_h, orig_w = frame.shape[:2]

        # Choose the result instance (index) with largest bounding box
        bboxes_xyxy = entry['pred_boxes_XYXY'].numpy()
        bboxes_area = (bboxes_xyxy[:, 2] - bboxes_xyxy[:, 0]) \
                      * (bboxes_xyxy[:, 3] - bboxes_xyxy[:, 1])
        largest_bbox_index = np.argmax(bboxes_area)

        largest_bbox = bboxes_xyxy[largest_bbox_index].astype(np.int16)
        result_encoded = entry['pred_densepose'].results[largest_bbox_index]
        iuv_arr = DensePoseResult.decode_png_data(*result_encoded)

        # # Round bbox to int
        # rounded_largest_bbox =

        I_image = np.zeros(orig_h, orig_w)
        I_image[largest_bbox[0]:largest_bbox[2],
        largest_bbox[1]:largest_bbox[3]] = iuv_arr[0, :, :]
        print(I_image.shape)
        plt.imshow(I_image/24)
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump_file', type=str)
    args = parser.parse_args()

    visualise_denspose_results(args.dump_file)
