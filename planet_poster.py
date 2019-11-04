# Copyright [2019] [Hayden Nix]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Inspired by and based on project by Eric Davidson (@ericdavidson)

import argparse
import cairo
import math
import random

from PIL import Image, ImageDraw

list_of_colors = [[145, 185, 141], [229, 192, 121], [210, 191, 88],
                  [140, 190, 178], [255, 183, 10], [189, 190, 220],
                  [221, 79, 91], [16, 182, 98], [227, 146, 80],
                  [241, 133, 123], [110, 197, 233], [235, 205, 188],
                  [197, 239, 247], [190, 144, 212], [41, 241, 195],
                  [101, 198, 187], [255, 246, 143], [243, 156, 18],
                  [189, 195, 199], [243, 241, 239]]


def main():
    normalize_color(list_of_colors[1])
    args = parse_args()
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, args.width, args.height)
    ctx = cairo.Context(surface)

    draw_background(ctx, .3, .3, .3, args.width, args.height)
    # Draw sun
    sun_color = normalize_color(random.choice(list_of_colors))
    draw_circle_fill(ctx, args.width / 2, args.height - args.bordersize,
                     args.sunsize, sun_color[0], sun_color[1], sun_color[2])

    draw_planets(ctx, args, 5, 70, 20, sun_color)
    surface.write_to_png("planets.png")

    # Draw border
    draw_border(ctx, args.bordersize, sun_color[0], sun_color[1], sun_color[2],
                args.width, args.height)
    texturize("planets.png", "planets_texturized.png")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", default=3000, type=int)
    parser.add_argument("--height", default=2000, type=int)
    parser.add_argument("-o", "--orbit", action="store_true")
    parser.add_argument("-l", "--line", action="store_true")
    parser.add_argument("-s", "--sunsize", default=200, type=int)
    parser.add_argument("-bs", "--bordersize", default=50, type=int)
    return parser.parse_args()


def draw_background(ctx, r, g, b, width, height):
    ctx.set_source_rgb(r, g, b)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()


def draw_border(ctx, size, r, g, b, width, height):
    ctx.set_source_rgb(r, g, b)
    ctx.rectangle(0, 0, size, height)
    ctx.rectangle(0, 0, width, size)
    ctx.rectangle(0, height - size, width, size)
    ctx.rectangle(width - size, 0, size, height)
    ctx.fill()


def draw_circle_fill(ctx, x, y, radius, r, g, b):
    ctx.set_source_rgb(r, g, b)
    ctx.arc(x, y, radius, 0, 2 * math.pi)
    ctx.fill()


def draw_planets(ctx, args, min_size, max_size, seperation_distance,
                 sun_color):
    distance_between_planets = 20
    last_center = args.height - args.bordersize
    last_size = args.sunsize
    last_color = sun_color

    min_size = 5
    max_size = 70

    for x in range(1, 20):
        next_size = random.randint(min_size, max_size)
        next_center = last_center - last_size - (next_size *
                                                 2) - distance_between_planets

        if not (next_center - next_size < args.bordersize):
            if (args.orbit):
                draw_orbit(ctx, 4, args.width / 2,
                           args.height - args.bordersize,
                           args.height - next_center - args.bordersize, .6, .6,
                           .6)
            elif (args.line):
                ctx.move_to(args.bordersize * 2, next_center)
                ctx.line_to(args.width - (args.bordersize * 2), next_center)
                ctx.stroke()

            draw_circle_fill(ctx, args.width / 2, next_center, next_size * 1.3,
                             .3, .3, .3)

            rand_color = random.choice(list_of_colors)
            while (rand_color is last_color):
                rand_color = random.choice(list_of_colors)

            last_color = rand_color

            r, g, b = rand_color[0] / 255.0, rand_color[1] / 255.0, rand_color[
                2] / 255.0

            draw_circle_fill(ctx, args.width / 2, next_center, next_size, r, g,
                             b)

            last_center = next_center
            last_size = next_size

            min_size += 5
            max_size += 5 * x


def draw_orbit(ctx, line, x, y, radius, r, g, b):
    ctx.set_line_width(line)
    ctx.arc(x, y, radius, 0, 2 * math.pi)
    ctx.stroke()


def normalize_color(color):
    for i, v in enumerate(color):
        color[i] = v / 255.0
    return color


def texturize(image, output):
    pil_image = Image.open(image)
    pixels = pil_image.load()

    for i in range(pil_image.size[0]):
        for j in range(pil_image.size[1]):
            r, g, b = pixels[i, j]

            noise = random.uniform(0.6, 1.4)
            pixels[i, j] = (int(r * noise), int(g * noise), int(b * noise))
    pil_image.save("planets_textured.png")


if __name__ == "__main__":
    main()