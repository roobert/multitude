#!/usr/bin/env python

# from firebase_admin import credentials
# cred = credentials.Certificate("path/to/serviceAccount.json")
# firebase_admin.initialize_app(cred)

import sys
import argparse
import firebase_admin
from dataclasses import dataclass
from firebase_admin import firestore


@dataclass
class MultitudeClient:
    collection: str
    owner: str
    repo: str
    status: str
    tag: str

    def __post_init__(self):
        self.db_configure()

    def db_configure(self):
        firebase_admin.initialize_app()
        self.db = firestore.client()

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
