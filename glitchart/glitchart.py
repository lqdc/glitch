#!/usr/bin/env python3
# -*- coding utf-8 -*-
# @author: Roman Sinayev
# @created: 2017-08-03 05:16:20
# @modified: 2017-08-03 20:14:36
# @filename: glitchart.py


import copy
import io
import os
import random

from PIL import Image

MAX_RETRIES = 3


class BadImgException(Exception):
    pass


def glitch(data, n_iter=None, amnt=None, seed=None, verbose=False):
    found = data.find(bytes((255, 218)))
    if not found:
        raise BadImgException('Not a valid JPEG!')
    header_len = found + 2
    amnt = min(amnt, 1.) if amnt is not None else random.random()
    seed = min(seed, 1.) if seed is not None else random.random()
    n_iter = min(n_iter, 115) if n_iter is not None else random.randint(0, 115)

    if verbose:
        print('Data length: %s' % len(data))
        print('Amount: %s | Seed: %s | n_iter: %s' % (amnt, seed, n_iter))

    max_idx = len(data) - header_len - 4
    window_sz = max_idx // n_iter
    data_copy = bytearray(copy.copy(data))
    for i in range(header_len, max_idx, window_sz):
        mod_idx = i + int(window_sz * seed)
        mod_idx = min(mod_idx, max_idx)
        data_copy[mod_idx] = int(amnt * 256 / 100)
    return data_copy


def data_from_png(path):
    im = Image.open(path)
    im.convert('RGB')
    out = io.BytesIO()
    im.save(out, quality=95, format='JPEG')
    out.seek(0)
    return out.read()


def img_to_png(data, path):
    try:
        stream = io.BytesIO(data)
        im = Image.open(stream)
        im.save(path)
    except Exception as err:
        raise BadImgException(err)


def convert_img(img_path):
    extension = os.path.splitext(img_path)[-1]
    if extension == '.png':
        return data_from_png(img_path)
    elif extension in ('.jpg', '.jpeg', '.jpe'):
        with open(img_path, 'rb') as f:
            return f.read()
    else:
        raise BadImgException('Unknown image extension: %s' % (extension,))


def data_to_jpg(data, path):
    with open(path, 'wb') as f:
        f.write(data)


def retry_glitch(data, n_iter, amnt, seed, path, verbose=False):
    max_retr = MAX_RETRIES
    new_data = bytearray(data)
    while max_retr:
        new_data = glitch(new_data, n_iter=n_iter, amnt=amnt, seed=seed, verbose=verbose)
        try:
            extension = os.path.splitext(path)[-1].lower()
            if extension in ('.jpg', '.jpeg', '.jpe'):
                data_to_jpg(new_data, path)
            elif extension == '.png':
                img_to_png(new_data, path)
            else:
                raise ValueError('Unknown extension for output path: %s' % (extension,))

            if verbose:
                print('Saved to path %s' % path)
            return
        except BadImgException:
            max_retr -= 1
            if n_iter >= 10:
                if verbose:
                    print('Bad image.. retrying... Retries left %d' % (max_retr,))
                n_iter = int(0.9 * n_iter)
            else:
                raise


def resize(data, max_width):
    inp = io.BytesIO(data)
    img = Image.open(inp)
    if img.size[0] > max_width:
        wpercent = (max_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((max_width, hsize), Image.ANTIALIAS)
        out = io.BytesIO()
        img.save(out, quality=95, format='JPEG')
        img.close()
        out.seek(0)
        return out.read()
    else:
        return data


def glitch_main():
    import argparse
    parser = argparse.ArgumentParser(prog='glitchart', description='Glitch art generator')
    parser.add_argument('img_path', type=str, help='Path to image to make glitch art from.')
    parser.add_argument('--amount', type=float, default=random.random(), help='Amount to change pixels by (0 - 1). Default random float 0-1.')
    parser.add_argument('--seed', type=float, default=random.random(), help='Location of pixel changed within a window. Default random float 0-1.')
    parser.add_argument('--n_iter', type=int, default=random.randint(0, 40), help='Number of pixels (windows) to change. Default random int 0-40.')
    parser.add_argument('--max_width', type=int, default=900, help='Maximum width of image before resizing and keeping aspect ratio. Default 900.')
    parser.add_argument('--output_path', type=str, default=None, help='Output image path. By default appends _glitched to filename')
    parser.add_argument('--png', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true', help='Silence stdout.')
    parsed = parser.parse_args()

    data = convert_img(parsed.img_path)
    data = resize(data, parsed.max_width)
    ext = '.png' if parsed.png else '.jpg'
    if parsed.output_path is not None:
        out_path = parsed.out_path
    else:
        out_path = os.path.splitext(parsed.img_path)[0] + '_glitched' + ext

    retry_glitch(data, parsed.n_iter, parsed.amount, parsed.seed, out_path, verbose=(not parsed.quiet))


if __name__ == '__main__':
    glitch_main()
