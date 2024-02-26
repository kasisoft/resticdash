[![StandWithUkraine][ukraine-svg]][ukraine-readme]

# ResticDash

## Motivation

[restic] itself is a popular backup tool which works pretty reliable and efficiently.
I'm running several backups in my homelab on a time schedule.
In general there shouldn't be any issue with that but how can I be sure?

That's where this dashboard comes in. It's meant to visually show if a backup ran in a specified timeframe. If it ran it's green and otherwise it will simply be red, so I might need to check in on that.

Another reason for this dashboard is the fact that Ilike to dabble in other unfamiliar technologies as I'm primarily a Java/Kotlin/Spring dev.
So this little dashboard serves as a useful playground and a way to practice other stuff.


## A note of caution

* I myself am neither a [python] nor a frontend developer. So the codebase is based upon a very small skillset.

* Everything is based on Linux as it's meant to be used for myself. However I appreciate any kind of feedback to improve or fix my codebase.

* The UI isn't very appealing as I clearly have no talent for visual stuff. Suggestions are welcome.



## Repository Structure

This repository contains the following directories:


### fs

This is a simple directory with several bash scripts used to setup some [restic] repositories which is useful for testing purposes.

Further information can be found here: [README.md](./fs/README.md)


### backend

The __backend__ has been written in [python] and provides a basic REST server as well as the frontend code.

Further information can be found here: [README.md](./backend/README.md)


### frontend

The __frontend__ has been written using [svelte] and especially Svelte 5 and it's runes which makes life for frontend developers much easier.

Further information can be found here: [README.md](./frontend/README.md)


### install

The __install__ directory is just a collection of scripts and files allowing to configure a Linux service making use of this dashboard.

Further information can be found here: [README.md](./install/README.md)


## License

[MIT][license] © [Kasisoft.com] - <daniel.kasmeroglu@kasisoft.com>


[arktype]: https://arktype.io/
[axios]: https://axios-http.com/docs/intro
[flask]: https://flask.palletsprojects.com/en/3.0.x/
[flowbite]: https://flowbite.com/
[kasisoft.com]: https://kasisoft.com
[license]: ./LICENSE
[pex]: https://docs.pex-tool.org/
[pnpm]: https://pnpm.io/
[python]: https://www.python.org/
[restic]: https://restic.net/
[resticpy]: https://github.com/mtlynch/resticpy
[svelte]: https://svelte.dev/
[tailwindcss]: https://tailwindcss.com/
[typescript]: https://www.typescriptlang.org/
[vite]: https://vitejs.dev/
[yaml]: https://yaml.org/

[ukraine-readme]: https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md
[ukraine-svg]: https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg