#!/usr/bin/env python
#
# FIXME: prototype
#

import os
import secrets
import logging
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from firestore.client import MultitudeClient
from firestore.doc import MultitudeDoc
from secret import get_secret

app = FastAPI()
security = HTTPBasic()

auth_username = os.environ["MULTITUDE_USERNAME"]
auth_password = os.environ["MULTITUDE_PASSWORD"]

logger = logging.getLogger("api")

secret = get_secret()
app.secret_key = secret
logger.debug(f"token: {secret}")

multitude_client = MultitudeClient()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://localhost",
        "https://localhost:8080",
        "http://localhost",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def authorized(username, password):
    correct_username = secrets.compare_digest(
        username, os.environ.get("MULTITUDE_USERNAME")
    )
    correct_password = secrets.compare_digest(
        password, os.environ.get("MULTITUDE_PASSWORD")
    )
    return correct_username and correct_password


@app.put("/upsert/{collection}/{owner}/{repo}/{tag}")
def upsert(
    collection: str,
    owner: str,
    repo: str,
    tag: str,
    status: str = None,
    credentials: HTTPBasicCredentials = Depends(security),
):
    if not authorized(credentials.username, credentials.password):
        return "Authorization failure", 401

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
def fetch_collection(
    collection, credentials: HTTPBasicCredentials = Depends(security),
):
    if not authorized(credentials.username, credentials.password):
        return "Authorization failure", 401

    doc = MultitudeDoc(db=multitude_client.db, collection=collection)
    return doc.fetch_collection()


@app.get("/fetch/{collection}/{owner}")
def fetch_collection_owner(
    collection, owner=None, credentials: HTTPBasicCredentials = Depends(security),
):
    if not authorized(credentials.username, credentials.password):
        return "Authorization failure", 401

    doc = MultitudeDoc(db=multitude_client.db, collection=collection, owner=owner)
    return doc.fetch_collection_owner()


@app.get("/fetch/{collection}/{owner}/{repo}")
def fetch_collection_owner_repo(
    collection,
    owner=None,
    repo=None,
    credentials: HTTPBasicCredentials = Depends(security),
):
    if not authorized(credentials.username, credentials.password):
        return "Authorization failure", 401

    doc = MultitudeDoc(
        db=multitude_client.db, collection=collection, owner=owner, repo=repo
    )
    return doc.fetch_collection_owner_repo()


@app.get("/fetch/{collection}/{owner}/{repo}/{tag}")
def fetch_collection_owner_repo_tag(
    collection,
    owner=None,
    repo=None,
    tag=None,
    credentials: HTTPBasicCredentials = Depends(security),
):
    if not authorized(credentials.username, credentials.password):
        return "Authorization failure", 401

    doc = MultitudeDoc(
        db=multitude_client.db, collection=collection, owner=owner, repo=repo, tag=tag
    )
    return doc.fetch_collection_owner_repo_tag()
