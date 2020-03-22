#!/usr/bin/env python

from string import ascii_letters, punctuation, digits
from random import randint, choice
from os import environ


def get_secret():
    return (
        environ["MULTITUDE_TOKEN"]
        if environ.get("MULTITUDE_TOKEN")
        else generate_secret()
    )


def generate_secret():
    characters = ascii_letters + punctuation + digits
    return "".join(choice(characters) for x in range(randint(20, 20)))
