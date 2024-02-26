[![StandWithUkraine][ukraine-svg]][ukraine-readme]

# Prerequisites

The following applications/features need to be installed:

* Python
* Virtualenv
* Restic


# Setup

## Virtualenv

```bash
cd backend
virtualenv venv
source ./venv/bin/activate
pip3 install -r ./requirements.txt
```

# Build

You can build a [pex] file which contains all dependencies except for the [python] interpreter using the script [pexbuild.sh] while passing the main module to be used as the entrypoint.

Example:

```bash
cd backend

# this will generate a file 'app.pex' in this directory
./pexbuild.sh resticdash.main:main
```




[pexbuild.sh]: ./pexbuild.sh


[pex]: https://docs.pex-tool.org/

[ukraine-readme]: https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md
[ukraine-svg]: https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg
