#!/usr/bin/env python

import os
import sys
import argparse
import firebase_admin
from dataclasses import dataclass, field
from firebase_admin import firestore


class CredentialsError(Exception):
    pass


@dataclass
class MultitudeClient:
    collection: str
    owner: str = field(init=False)
    repo: str = field(init=False)
    status: str = field(init=False)
    tag: str = field(init=False)

    def __post_init__(self):
        self.db_configure()

    def db_configure(self):
        if os.environ["MULTITUDE_SERVICE_ACCOUNT_KEY"]:
            credentials = firebase_admin.credentials.Certificate(
                os.environ["MULTITUDE_SERVICE_ACCOUNT_KEY"]
            )
            firebase_admin.initialize_app(credentials)
        elif os.environ["FIRESTORE_EMULATOR_HOST"]:
            firebase_admin.initialize_app()
        else:
            raise CredentialsError(
                "MULTITUDE_SERVICE_ACCOUNT_KEY or FIRESTORE_EMULATOR_HOST not set!"
            )

        self.db = firestore.client()

    def fetch(self):
        docs = self.db.collection(self.collection).stream()
        return docs

    def dump(self):
        docs = self.db.collection(self.collection).stream()
        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")

    # FIXME
    # * there is probably a better way to do this..
    def upsert(self):
        docs = (
            self.db.collection(self.collection)
            .where("owner", "==", self.owner)
            .where("repo", "==", self.repo)
            .where("properties.tag", "==", self.tag)
        )

        updated = False

        for data in docs.stream():
            doc = data.to_dict()

            if not doc["owner"] == self.owner:
                continue
            if not doc["repo"] == self.repo:
                continue
            if not doc["properties"]["tag"] == self.tag:
                continue

            doc = self.db.collection(self.collection).document(data.id)

            doc.update(
                {
                    "timestamp": firestore.SERVER_TIMESTAMP,
                    "owner": self.owner,
                    "repo": self.repo,
                    "properties": {"status": self.status, "tag": self.tag},
                }
            )
            updated = True

        if not updated:
            doc = self.db.collection(self.collection).document()
            doc.set(
                {
                    "timestamp": firestore.SERVER_TIMESTAMP,
                    "owner": self.owner,
                    "repo": self.repo,
                    "properties": {"status": self.status, "tag": self.tag},
                }
            )


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


def main():
    args = parse_args()

    muc = MultitudeClient(
        collection=args.collection,
        owner=args.owner,
        repo=args.repository,
        status=args.status,
        tag=args.tag,
    )

    muc.upsert()


if __name__ == "__main__":
    main()
