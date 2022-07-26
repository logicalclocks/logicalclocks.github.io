import argparse
import shutil
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', help="path to the hopsworks tutorials dir", type=str, default="docs/hopsworks-tutorials")
    parser.add_argument('--src', '-s', help="name of directory with images to copy", type=str, default="images")

    args = parser.parse_args()

    except_dirs = [".git", args.src]

    sub_dirs = [
        element for element in os.listdir(args.path)
        if os.path.isdir(os.path.join(args.path, element)) and element not in except_dirs
    ]

    for dst in sub_dirs:
        shutil.copytree(os.path.join(args.path, args.src), os.path.join(args.path, dst, args.src), dirs_exist_ok=True)
