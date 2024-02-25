#!/bin/bash

export PASSWORDS=("e3a9abaa-6089-4973-98b2-1fceb481452c" "c2f19138-6d65-4269-a2cd-2072b2648ba6" "3b5c75c7-dd34-4c93-b25e-0af2e5da0ddc" "a9d60700-1b68-4efd-acb7-ab28108066cc")
export BACKUPS=("backups/none" "backups/one" "backups/two" "backups/many")

export DIRNAME=$(readlink -f $(dirname .))
export CONTENTDIR="${DIRNAME}/content"

export SOURCEDIRS=("content/dir1" "content/dir2")

mkdir -p "${DIRNAME}/${SOURCEDIRS[0]}"
mkdir -p "${DIRNAME}/${SOURCEDIRS[1]}"

init_repo() {
    index="$1"
    export RESTIC_REPOSITORY="${DIRNAME}/${BACKUPS[$index]}"
    export RESTIC_PASSWORD="${PASSWORDS[$index]}"
    restic --no-cache init
}

backup_repo() {
    index="$1"
    dirindex="$2"
    export RESTIC_REPOSITORY="${DIRNAME}/${BACKUPS[$index]}"
    export RESTIC_PASSWORD="${PASSWORDS[$index]}"
    restic --no-cache backup "${DIRNAME}/${SOURCEDIRS[$dirindex]}"
}


list_snapshots() {
    index="$1"
    export RESTIC_REPOSITORY="${DIRNAME}/${BACKUPS[$index]}"
    export RESTIC_PASSWORD="${PASSWORDS[$index]}"
    restic --no-cache snapshots
}


list_snapshots_json() {
    index="$1"
    export RESTIC_REPOSITORY="${DIRNAME}/${BACKUPS[$index]}"
    export RESTIC_PASSWORD="${PASSWORDS[$index]}"
    restic --no-cache --json snapshots >/tmp/out.json
    jq . /tmp/out.json
}

