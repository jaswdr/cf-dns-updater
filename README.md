# CloudFlare DNS Updater

> Monitors and update DNS records in CloudFlare.

## Usage

Set environment variables:

- `CLOUDFLARE_API_TOKEN`: CloudFlare API token
- `CLOUDFLARE_ZONE_NAME`: CloudFlare zone name (e.g. `example.com`)
- `CLOUDFLARE_DNS_NAME`: CloudFlare DNS record name (e.g. `www`)
- `CLOUDFLARE_DNS_TYPE`: CloudFlare record type (default: `A`)
- `IP_SOURCE_URL`: URL to fetch the IP from (default: `https://api.ipify.org`)
- `POLL_INTERVAL`: Interval between IP checks (default: `5m`)

Run the script:

```sh
$ ./main.py
# Starting CloudFlare IP Updater...
```

The script will run in the foreground and log to stdout. It will check the DNS record every `POLL_INTERVAL` and update the record if it doesn't match.

## Docker

Create a .env file with the environment variables:

```text
CLOUDFLARE_API_TOKEN=...
CLOUDFLARE_ZONE_NAME=example.com
CLOUDFLARE_DNS_NAME=www
CLOUDFLARE_DNS_TYPE=A
```

Then run the container:

```sh
$ docker run --env-file=.env ghcr.io/jaswdr/cf-dns-updater:master
# ...
# Starting CloudFlare DNS Updater...
```

## License

[MIT](LICENSE)
