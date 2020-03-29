#!/usr/bin/env python

from os import environ
import firebase_admin
from dataclasses import dataclass, field
from firebase_admin import firestore


class CredentialsError(Exception):
    pass


@dataclass
class MultitudeClient:
    db: any = field(init=False)

    def __post_init__(self):
        if environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            credentials = firebase_admin.credentials.Certificate(
                environ["GOOGLE_APPLICATION_CREDENTIALS"]
            )
            firebase_admin.initialize_app(credentials)
        elif environ.get("FIRESTORE_EMULATOR_HOST"):
            firebase_admin.initialize_app()
        else:
            raise CredentialsError(
                "not set: GOOGLE_APPLICATION_CREDENTIALS or FIRESTORE_EMULATOR_HOST"
            )

        self.db = firestore.client()

    def __getattr__(self, name):
        def method(*args):
            getattr(self.db, name, *args)

        return method
