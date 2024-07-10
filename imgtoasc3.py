#!/usr/bin/env python3

from PIL import Image
import argparse

parser = argparse.ArgumentParser(
                    prog='image to ASCII',
                    description='transfers images to text')

parser.add_argument('filename', type=str, help="path to image")
parser.add_argument('output', type=str, help="path to text output")
parser.add_argument('-W', '--width', type=int, default=30, help='width of text-image, default is 30')
parser.add_argument('-H', '--height', type=int, default=30, help='height of text-image, default is 30')
parser.add_argument('-t', '--threshold', type=int, default=127, help='color threshold, default is 127')
parser.add_argument('-r', '--reverse', action='store_true', help='reverse image, default is false')
args = parser.parse_args()

with Image.open(args.filename) as img:
    img.load()

img = img.convert("LA")
width = args.width
height = args.height
img = img.resize((width * 2, height * 4))
nums = [[0] * (height * 4) for _ in range(width * 2)]
asc = [[""] * width for _ in range(height)]

def get_symbol(m, n):
    smb = 10240
    for i in range(2):
        for j in range(3):
            smb += (2 ** (i * 3 + j)) if bool(nums[m + i][n + j] > args.threshold) ^ bool(args.reverse) else 0
    smb += (2 ** 6) if bool(nums[m][n + 3] > args.threshold) ^ bool(args.reverse) else 0
    smb += (2 ** 7) if bool(nums[m + 1][n + 3] > args.threshold) ^ bool(args.reverse) else 0
    return "⢀" if smb == 10240 else chr(smb)

for i in range(width * 2):
    for j in range(height * 4):
        gamma = img.getpixel((i, j))
        nums[i][j] = (gamma[0] + gamma[1]) // 2 if gamma[1] < 127 else gamma[0]

for i in range(width):
    for j in range(height):
        asc[j][i] = get_symbol(i * 2, j * 4)

with open(args.output, "w+", encoding="UTF-8") as out:
    for i in asc:
        out.write("".join(i) + '\n')
        print("".join(i))