
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import imageio
import argparse
from models import GaussianModel, AdaptiveGaussianModel

# 2141 frames in total
TOTAL_FRAMES = 2141
#PERCENTAGE = 0.25
#ALPHA = 11
#P = 0.001

VIDEO_PATH = "../../AICity_data/train/S03/c010/vdo.avi"

def post_processing(foreground):
    return foreground


def main(args):

    if not os.path.exists(VIDEO_PATH):
        print("Video does not exist.")
        return

    model_frames = int(args.percentage * TOTAL_FRAMES)

    if args.model == "gm":
        model = GaussianModel(VIDEO_PATH, model_frames, args.alpha, f"{args.percentage}")
        MODEL_NAME = "GaussianModel"
    elif args.model == "agm":
        model = AdaptiveGaussianModel(VIDEO_PATH, model_frames, args.alpha, args.p, f"{args.percentage}")
        MODEL_NAME = "AdaptiveGaussianModel"
    else:
        raise Exception

    model.model_background()

    results_path = f"results/{MODEL_NAME}/{args.alpha}_{args.percentage}"
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    writer = imageio.get_writer(f"{results_path}/video.mp4", fps=25)

    foreground = model.compute_next_foreground()
    writer.append_data(foreground)
    counter = 0
    while foreground is not None:
        foreground = post_processing(foreground)
        #cv2.imwrite(f"results/{args.alpha}_{args.percentage}/fg_{counter}.png", foreground)
        writer.append_data(foreground)
        counter += 1

        foreground = model.compute_next_foreground()
        if counter % 500 == 0:
            print(f"[{counter}]")

        if args.max != -1 and counter >= args.max:
            break

    print(f"DONE! {counter} frames processed")
    writer.close()
    print(f"Saved to '{results_path}'")


parser = argparse.ArgumentParser(description='Extract foreground from video.')
parser.add_argument('-m', '--model', type=str, default='gm', choices=["gm", "agm"], help="model used for background modeling")
parser.add_argument('-M', '--max', type=int, default=-1, help="max of frames for which infer foreground")
parser.add_argument('-perc', '--percentage', type=float, default=0.25, help="percentage of video to use for background modeling")
parser.add_argument('-a', '--alpha', type=float, default=11, help="alpha value")
parser.add_argument('-p', '--p', type=float, default=0.001, help="[AdaptiveGaussianModel] parameter controlling the inclusion of new information to model")
args = parser.parse_args()

main(args)