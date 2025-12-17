#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os

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

def get_text_content(text_arg):
    """Reads text from a file if the argument is a valid file path, otherwise returns the argument."""
    if text_arg and os.path.isfile(text_arg):
        with open(text_arg, "r", encoding="utf-8") as f:
            return f.read()
    return text_arg