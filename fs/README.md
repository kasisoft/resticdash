[![StandWithUkraine][ukraine-svg]][ukraine-readme]

# Prerequisites

* [restic] must be installed
* [jq] must be installed (used for formatted json)


# FS

The most important script in this folder is [common.sh](./common.sh) as it contains all functions being invoked by the following wrapper scripts:

* [backup.sh]
* [snapshots-json.sh] 
* [snapshots.sh]

* [random-files.sh]

In order to start you need to run [init.sh] first which will create the following sub directories:

* backups - this will contain 4 restic repositories.
* content - this will contain two base directories with random files.

If you want to change the "content" you can rerun the script [random-files.sh].

The other scripts will accept numerical parameters whereas the first must be a value between 0 to 3 in order to select a [restic] repository (see [common.sh] for insights).

[backup.sh] accepts a second numerical parameter which can be 0 or 1 in order to backup a content tree from the subdirectory ___content___.

Examples:

```bash
# Backup the second directory 'dir1' in the second repository 'one'
./backup.sh 1 1

# Lists all snapshots of the repository 'two'
./snapshots.sh 2

# Lists all snapshots of the repository 'two' and prints it's json representation
./snapshots-json.sh 2
```



[backup.sh]: ./backup.sh
[common.sh]: ./common.sh
[init.sh]: ./init.sh
[random-files.sh]: ./random-files.sh
[snapshots-json.sh]: ./snapshots-json.sh
[snapshots.sh]: ./snapshots.sh

[jq]: https://jqlang.github.io/jq/
[restic]: https://restic.net/

[ukraine-readme]: https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md
[ukraine-svg]: https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg
