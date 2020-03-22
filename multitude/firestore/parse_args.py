#!/usr/bin/env python

import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="multitude client")

    parser.add_argument("-c", "--collection", help="specify collection", required=True)
    parser.add_argument("-o", "--owner", help="specify owner", required=True)
    parser.add_argument("-r", "--repository", help="specify repository", required=True)
    parser.add_argument("-t", "--tag", help="specify tag", required=True)
    parser.add_argument("-s", "--status", help="specify status", required=True)

    if len(sys.argv) == 0:
        parser.print_help()
        exit(1)

    return parser.parse_args()
