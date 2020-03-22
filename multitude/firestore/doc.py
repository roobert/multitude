#!/usr/bin/env python

from dataclasses import dataclass, asdict
from firebase_admin import firestore

# from .client import MultitudeClient


@dataclass
class MultitudeDoc:
    db: any
    collection: str
    owner: str = ""
    repo: str = ""
    status: str = ""
    tag: str = ""

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
        updated = False
        print(type(self.db))

        docs = (
            self.db.collection(self.collection)
            .where("owner", "==", self.owner)
            .where("repo", "==", self.repo)
            .where("properties.tag", "==", self.tag)
        )

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

        return asdict(self)
