from fetcher.client import Client


def make_client(options):
    return Client(retries=options["retries"])


def run(path, options, out):
    client = make_client(options)
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            url = line.strip()
            if url and not url.startswith("#"):
                out.write(f"{url} {len(client.get(url))}\n")
