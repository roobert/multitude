#!/usr/bin/env python

import logging
from fastapi import FastAPI
from firestore.client import MultitudeClient
from firestore.doc import MultitudeDoc
from secret import get_secret

app = FastAPI()

logger = logging.getLogger("api")

secret = get_secret()
app.secret_key = secret
logger.debug(f"token: {secret}")

multitude_client = MultitudeClient()


@app.put("/upsert/{collection}/{owner}/{repo}/{tag}")
def upsert(collection: str, owner: str, repo: str, tag: str, status: str = None):
    if not status:
        return "status parameter not specified", 400

    doc = MultitudeDoc(
        db=multitude_client.db,
        collection=collection,
        owner=owner,
        repo=repo,
        tag=tag,
        status=status,
    )
    return doc.upsert()


@app.get("/fetch/{collection}")
def fetch_collection(collection):
    doc = MultitudeDoc(db=multitude_client.db, collection=collection)
    return doc.fetch_collection()


@app.get("/fetch/{collection}/{owner}")
def fetch_collection_owner(collection, owner=None):
    doc = MultitudeDoc(db=multitude_client.db, collection=collection, owner=owner)
    return doc.fetch_collection_owner()


@app.get("/fetch/{collection}/{owner}/{repo}")
def fetch_collection_owner_repo(collection, owner=None, repo=None):
    doc = MultitudeDoc(
        db=multitude_client.db, collection=collection, owner=owner, repo=repo
    )
    return doc.fetch_collection_owner_repo()


@app.get("/fetch/{collection}/{owner}/{repo}/{tag}")
def fetch_collection_owner_repo_tag(collection, owner=None, repo=None, tag=None):
    doc = MultitudeDoc(
        db=multitude_client.db, collection=collection, owner=owner, repo=repo, tag=tag
    )
    return doc.fetch_collection_owner_repo_tag()
