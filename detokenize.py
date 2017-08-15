#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Gabor L Ugray

"""Detokenize text with OpenNMT separator and features (if present)
"""

from __future__ import print_function, unicode_literals, division
import sys
import codecs
import io
import argparse
from collections import defaultdict
from math import log, exp

# hack for python2/3 compatibility
from io import open
argparse.open = open


def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Detokenize text with OpenNMT separator and features (if present)")

    parser.add_argument(
        '--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
        metavar='PATH',
        help="Input file (default: standard input).")
    parser.add_argument(
        '--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
        metavar='PATH',
        help="Output file (default: standard output)")

    return parser

def apply_case(norm, feat):
  if feat == 'N': return norm
  if feat == 'A': return norm.upper()
  if feat == 'S': return norm[0].upper() + norm[1:]
  without_sep = norm
  start_sep = ''
  end_sep = ''
  if without_sep.endswith('￭'):
    end_sep = '￭'
    without_sep = without_sep[:-1]
  if without_sep.startswith('￭'):
    start_sep = '￭'
    without_sep = without_sep[1:]
  if feat == 'E': without_sep = without_sep[:-1] + without_sep[-1].upper()
  if feat == 'B': without_sep = without_sep[0].upper() + without_sep[1:]
  return start_sep + without_sep + end_sep

if __name__ == '__main__':

    # python 2/3 compatibility
    if sys.version_info < (3, 0):
        sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
        sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
        sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
    else:
        sys.stderr = codecs.getwriter('UTF-8')(sys.stderr.buffer)
        sys.stdout = codecs.getwriter('UTF-8')(sys.stdout.buffer)
        sys.stdin = codecs.getreader('UTF-8')(sys.stdin.buffer)

    parser = create_parser()
    args = parser.parse_args()

    # read/write files as UTF-8
    if args.input.name != '<stdin>':
        args.input = codecs.open(args.input.name, encoding='utf-8')
    if args.output.name != '<stdout>':
        args.output = codecs.open(args.output.name, 'w', encoding='utf-8')

    for line in args.input:
      out_words = []
      for word in line.split():
        feat_pos = word.find('￨')
        if feat_pos == -1:
          out_words.append(word)
          continue
        norm = word[:feat_pos]
        feat = word[feat_pos + 1:]
        out_words.append(apply_case(norm, feat))

      out_line = ' '.join(out_words)
      out_line = out_line.replace('￭ ', '')
      out_line = out_line.replace(' ￭', '')

      args.output.write(out_line)
      args.output.write('\n')
