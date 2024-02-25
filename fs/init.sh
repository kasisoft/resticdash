#!/bin/bash

. ./common.sh

# setup our repos
init_repo 0
init_repo 1
init_repo 2
init_repo 3

# repo with one snapshots
backup_repo 1 0

# repo with 1wo snapshots
backup_repo 2 0
backup_repo 2 0

# repo with many snapshots
backup_repo 3 0
backup_repo 3 0
backup_repo 3 0
backup_repo 3 0

