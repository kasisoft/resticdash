[![StandWithUkraine][ukraine-svg]][ukraine-readme]


# Installation

Execute the script [install.sh] within your shell.
This will created the following directories:

* /opt/resticdash
* /etc/resticdash

_/opt/resticdash_ will contain the executable (.pex) as well as the frontend code in a subdirectory _/opt/resticdash/static_.

_/etc/resticdash_ will contain a file _resticdash.yaml_ which you need to configure to fit your needs.

After completing your configuration you need to install the service like this:

```bash
systemctl enable resticdash.service
systemctl daemon-reload
```


# Update

The update procedure is a simple as calling [update.sh]. 
This will stop and start the service while replacing the executable and the frontend code.


# Uninstallation

The script [uninstall.sh] will disable and remove the _resticdash_ service and remove all files in the aforementioned directories.


# Traefik

If you are using the popular reverse proxy [traefik] here's an example to put the _resticdash_ behind it. Obviously you need modifications to match your setup:

```yaml
http:
    routers:
        resticdash:
            entrypoints:
                - websecure   # the name depends on your general configuration
            rule: "Host(`my.homelab.com`) && PathPrefix(`/resticdash`)"
            service: resticdash
    services:
        resticdash:
            loadbalancer:
                servers:
                    - url: "http://174.144.2.19:3718/"
```


[install.sh]: ./install.sh
[uninstall.sh]: ./uninstall.sh
[update.sh]: ./update.sh

[traefik]: https://doc.traefik.io/traefik/

[ukraine-readme]: https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md
[ukraine-svg]: https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg