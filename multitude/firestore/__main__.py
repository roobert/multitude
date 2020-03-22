#!/usr/bin/env python

from parse_args import parse_args
from client import MultitudeClient
from doc import MultitudeDoc


def main():
    args = parse_args()

    doc = MultitudeDoc(
        db=MultitudeClient(),
        collection=args.collection,
        owner=args.owner,
        repo=args.repository,
        status=args.status,
        tag=args.tag,
    )

    doc.upsert()


if __name__ == "__main__":
    main()
