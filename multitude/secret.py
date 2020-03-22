#!/usr/bin/env python

from os import environ, urandom


def get_secret():
    return environ["MULTITUDE_TOKEN"] if environ["MULTITUDE_TOKEN"] else urandom(16)
