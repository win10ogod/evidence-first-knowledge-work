def upload_all(records, send):
    """Send every record to the ingestion API, one call per record."""
    calls = 0
    for record in records:
        send([record])
        calls += 1
    return calls
