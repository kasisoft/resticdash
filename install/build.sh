#!/bin/bash

export DIRNAME=$(readlink -f $(dirname $0))
export FRONTEND=$(readlink -f "${DIRNAME}/../frontend")
export BACKEND=$(readlink -f "${DIRNAME}/../backend")
export PACKAGEDIR="${DIRNAME}/resticdash"

export OLD_VERSION=$(jq .version "${FRONTEND}/package.json")
export OLD_VERSION="${OLD_VERSION%\"}"
export OLD_VERSION="${OLD_VERSION#\"}"

export GIT_SHORTID=$(git rev-parse --short HEAD)
export TAG="${OLD_VERSION}-${GIT_SHORTID}"

rm -rf "${PACKAGEDIR}"
mkdir -p "${PACKAGEDIR}"

echo "Building ResticDash PEX..."
cd ${BACKEND}
./pexbuild.sh resticdash.main:main


echo "Building Frontend Code..."
cd ${FRONTEND}
pnpm build


echo "Packaging ..."
cd ${DIRNAME}

mkdir -p "${PACKAGEDIR}/static"
cp -rp ${FRONTEND}/build/* "${PACKAGEDIR}/static/"

cp "${BACKEND}/app.pex" "${PACKAGEDIR}/resticdash.pex"

cp -rp ${DIRNAME}/resources/* "${PACKAGEDIR}/"

chmod +x "${PACKAGEDIR}/install.sh"
chmod +x "${PACKAGEDIR}/uninstall.sh"

echo "Creating archive..."
tar zcf "${DIRNAME}/resticdash-${TAG}.tgz" "resticdash/"
echo "Done"
