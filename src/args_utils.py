#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
import re

def init_parser(description):
    """Initialize an ArgumentParser with the given description."""
    return argparse.ArgumentParser(description=description)

def add_text_arg(parser, required=True):
    """Add the 'text' argument."""
    help_msg = "The text to convert or path to a text file"
    if required:
        parser.add_argument("text", help=help_msg)
    else:
        parser.add_argument("text", nargs="?", help=help_msg)

def add_outfile_arg(parser, required=True):
    """Add the 'outfile' argument."""
    help_msg = "The output file path (e.g. output.mp3)"
    if required:
        parser.add_argument("outfile", help=help_msg)
    else:
        parser.add_argument("outfile", nargs="?", help=help_msg)

def add_pitch_rate_args(parser):
    """Add --pitch and --rate arguments."""
    parser.add_argument("--pitch", default="+0Hz", help="Pitch adjustment (e.g. -50Hz)")
    parser.add_argument("--rate", default="+0%", help="Rate adjustment (e.g. -10%)")

def add_volume_arg(parser):
    """Add --volume argument."""
    parser.add_argument("--volume", default="+0%", help="Volume adjustment (e.g. +10%)")

def get_text_content(text_arg):
    """Reads text from a file if the argument is a valid file path, otherwise returns the argument."""
    if text_arg and os.path.isfile(text_arg):
        with open(text_arg, "r", encoding="utf-8") as f:
            return f.read()
    return text_arg

def parse_val(s):
    """Parses a string like '+10%' or '-5Hz' into (number, unit)."""
    if not s:
        return 0, ""
    m = re.match(r"([+-]?\d+)(.*)", s)
    if m:
        return int(m.group(1)), m.group(2)
    return 0, ""

def combine_values(base_s, offset_s):
    """Combines two value strings (e.g. '-10Hz' and '+5Hz')."""
    val1, unit1 = parse_val(base_s)
    val2, unit2 = parse_val(offset_s)
    # Prefer unit from base, or offset if base is empty
    unit = unit1 if unit1 else unit2
    total = val1 + val2
    sign = "+" if total >= 0 else ""
    return f"{sign}{total}{unit}"