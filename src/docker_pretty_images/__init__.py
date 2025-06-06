#!/usr/bin/env python3

import argparse
import subprocess
import json

# ANSI formatting
BOLD = '\033[1m'
ENDC = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
__version__ = "1.0.0"

def main():
    args = parse_args()

    if args.version:
        print(f"{BOLD}docker-pretty-images v{__version__}{ENDC}")
        return

    images = get_docker_images()

    # Filter out dangling images unless --all is used
    if not args.all:
        images = [img for img in images if img["Repository"] != "<none>" and img["Tag"] != "<none>"]

    # Apply ANSI colors to image names
    images = apply_colors_to_images(images)

    # Check usage for each image
    for img in images:
        img["in_use"] = is_image_in_use(img["ID"])

    # Print output
    print_images(images, slim=args.slim)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="docker-pretty-images",
        description="Minimal pretty printer for `docker images`"
    )
    parser.add_argument("-a", "--all", action="store_true", help="Include dangling images")
    parser.add_argument("-s", "--slim", action="store_true", help="Slim 1-line output")
    parser.add_argument("-v", "--version", action="store_true", help="Print version information")
    return parser.parse_args()


def get_docker_images():
    result = subprocess.run(
        ["docker", "images", "--format", "{{json .}}"],
        capture_output=True, text=True
    )
    return [json.loads(line) for line in result.stdout.strip().splitlines()]


def is_image_in_use(image_id):
    result = subprocess.run(
        ["docker", "ps", "-a", "--filter", f"ancestor={image_id}", "--format", "{{.ID}}"],
        capture_output=True,
        text=True
    )
    return bool(result.stdout.strip())


def apply_colors_to_images(images):
    colors = [
        '\033[94m',  # blue
        GREEN,
        RED,
        '\033[96m',  # cyan
        '\033[93m',  # yellow
        '\033[95m',  # magenta
    ]
    for index, img in enumerate(images):
        img["color"] = colors[index % len(colors)]
    return images


def print_images(images, slim=False):
    print("\nAll docker images")
    for img in images:
        print("")  # spacing
        colored_name = f"{img['color']}{BOLD}{img['Repository']}:{img['Tag']}{ENDC}"
        if slim:
            print(colored_name)
        else:
            print(colored_name)
            print_line("Image ID", img["ID"])
            print_line("Created", img["CreatedSince"])
            print_line("Size", img["Size"])
            if img["in_use"]:
                print_line("State", f"{GREEN}[In Use]{ENDC}")
            else:
                print_line("State", f"{RED}[Not Used]{ENDC}")
    print(f"\nTotal images:\t{len(images)}")



def print_line(label, value, width=24):
    print(f"\t{BOLD}{label}:{ENDC}".ljust(width), value)


if __name__ == "__main__":
    main()
