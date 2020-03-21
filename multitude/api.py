#!/usr/bin/env python

import os
from flask import Flask, request
from .multitude.firestore.client import MultitudeClient


app = Flask(__name__)

if os.environ["FLASK_DEBUG"] == "true":
    app.config["DEBUG"] = True


@app.route(
    "/update/<string:collection>/<string:owner>/<string:repo>/<string:tag>",
    methods=["PUT"],
)
def update(collection, owner, repo, tag):
    status = request.args.get("status")

    if not status:
        return "status parameter not specified", 400

    MultitudeClient(
        collection=collection, owner=owner, repo=repo, tag=tag, status=status,
    )
    return


@app.errorhandler(404)
def page_not_found(error):
    return "404", 404


if __name__ == "__main__":
    app.run()
