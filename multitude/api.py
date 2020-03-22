#!/usr/bin/env python

from flask import Flask, request
from firestore.client import MultitudeClient
from secret import get_secret


app = Flask(__name__)

secret = get_secret()
app.secret_key = secret
app.logger.debug(f"==> token: {secret}")


@app.route(
    "/upsert/<string:collection>/<string:owner>/<string:repo>/<string:tag>",
    methods=["PUT"],
)
def upsert(collection, owner, repo, tag):
    status = request.args.get("status")

    if not status:
        return "status parameter not specified", 400

    client = MultitudeClient(
        collection=collection, owner=owner, repo=repo, tag=tag, status=status,
    )
    client.update()
    return


@app.route(
    "/fetch/<string:collection>/<string:owner>/<string:repo>/<string:tag>",
    methods=["GET"],
)
def fetch_collection_owner_repo_tag(collection, owner=None, repo=None, tag=None):
    client = MultitudeClient(collection=collection, owner=owner, repo=repo, tag=tag)
    client.fetch()
    return


@app.route(
    "/fetch/<string:collection>/<string:owner>/<string:repo>", methods=["GET"],
)
def fetch_collection_owner_repo(collection, owner=None, repo=None):
    client = MultitudeClient(collection=collection, owner=owner, repo=repo)
    client.fetch()
    return


@app.route(
    "/fetch/<string:collection>/<string:owner>", methods=["GET"],
)
def fetch_collection_owner(collection, owner=None):
    client = MultitudeClient(collection=collection, owner=owner)
    client.fetch()
    return


@app.route(
    "/fetch/<string:collection>", methods=["GET"],
)
def fetch_collection(collection):
    client = MultitudeClient(collection=collection)
    client.fetch()
    return


@app.errorhandler(404)
def page_not_found(error):
    return "404", 404


if __name__ == "__main__":
    app.run()
