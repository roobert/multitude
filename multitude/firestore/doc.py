#!/usr/bin/env python

from dataclasses import dataclass
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

    # FIXME
    # * there is probably a better way to do this..
    def upsert(self):
        changed = []

        docs = (
            self.db.collection(self.collection)
            .where("owner", "==", self.owner)
            .where("repo", "==", self.repo)
            .where("properties.tag", "==", self.tag)
        )

        time_data = {"timestamp": firestore.SERVER_TIMESTAMP}
        doc_update = {
            "owner": self.owner,
            "repo": self.repo,
            "properties": {"status": self.status, "tag": self.tag},
        }

        for data in docs.stream():
            doc = data.to_dict()

            if not doc["owner"] == self.owner:
                continue
            if not doc["repo"] == self.repo:
                continue
            if not doc["properties"]["tag"] == self.tag:
                continue

            doc = self.db.collection(self.collection).document(data.id)
            doc.update({**doc_update, **time_data})
            changed.append(doc_update)

        if not changed:
            doc = self.db.collection(self.collection).document()
            doc.set({**doc_update, **time_data})
            changed.append(doc_update)

        return changed
