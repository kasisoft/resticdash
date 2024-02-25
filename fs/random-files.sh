#!/bin/bash

. ./common.sh

dd if=/dev/urandom of="${DIRNAME}/${SOURCEDIRS[0]}/file_a.bin" bs=1024 count=1

dd if=/dev/urandom of="${DIRNAME}/${SOURCEDIRS[1]}/file_a.bin" bs=1024 count=2
dd if=/dev/urandom of="${DIRNAME}/${SOURCEDIRS[1]}/file_b.bin" bs=1024 count=3
dd if=/dev/urandom of="${DIRNAME}/${SOURCEDIRS[1]}/file_c.bin" bs=1024 count=4

