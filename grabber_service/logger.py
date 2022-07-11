def printl(content):
    with open("/logs/sync.log", "a") as log:
        log.write(str(content))