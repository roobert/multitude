#!/usr/bin/env python

import logging
from fastapi import FastAPI, Request
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

    client = MultitudeDoc(
        db=multitude_client.db,
        collection=collection,
        owner=owner,
        repo=repo,
        tag=tag,
        status=status,
    )
    return client.upsert()


@app.get("/fetch/{collection}/{owner}/{repo}/{tag}")
def fetch_collection_owner_repo_tag(collection, owner=None, repo=None, tag=None):
    client = MultitudeDoc(
        db=multitude_client.db, collection=collection, owner=owner, repo=repo, tag=tag
    )
    return client.fetch()


@app.get("/fetch/{collection}/{owner}/{repo}")
def fetch_collection_owner_repo(collection, owner=None, repo=None):
    client = MultitudeDoc(
        db=multitude_client.db, collection=collection, owner=owner, repo=repo
    )
    return client.fetch()


@app.get("/fetch/{collection}/{owner}")
def fetch_collection_owner(collection, owner=None):
    client = MultitudeDoc(db=multitude_client.db, collection=collection, owner=owner)
    return client.fetch()


@app.get("/fetch/{collection}")
def fetch_collection(collection):
    client = MultitudeDoc(db=multitude_client.db, collection=collection)
    return client.fetch()
