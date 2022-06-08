import configparser
import io


def read_cfg(secret_name):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            config = configparser.RawConfigParser()
            sf_buf = io.StringIO(secret_file.read())
            config.read_file(sf_buf)
            return config["session"]["string"], config["api"]["id"], config["api"]["hash"]
    except IOError:
        print("error reading config secret!")
        return None


def read_pswd(secret_name):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return str(secret_file.readline()).replace("\n", "")
    except IOError:
        print("error reading db password secret!")
        return None
