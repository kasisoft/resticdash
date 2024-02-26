#!/bin/bash

export DIRNAME=$(readlink -f $(dirname .))
export FRONTEND=$(readlink -f "${DIRNAME}/../frontend")
export BACKEND=$(readlink -f "${DIRNAME}/../backend")
export PACKAGEDIR="${DIRNAME}/resticdash"

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
tar zcf "${DIRNAME}/resticdash.tgz" "resticdash/"
echo "Done"
