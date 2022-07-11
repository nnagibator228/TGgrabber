#!/bin/bash

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -i|--apiid)
      APIID="$2"
      shift
      shift
      ;;
    -h|--apihash)
      APIHASH="$2"
      shift
      shift
      ;;
    -s|--stringsession)
      STRINGSESSION="$2"
      shift
      shift
      ;;
    -d|--databasepassword)
      DATABASEPASS="$2"
      shift
      shift
      ;;
    -u|--adminuserid)
      ADMINUSER="$2"
      shift
      shift
      ;;
    -r|--rtoken)
      RTOKEN="$2"
      shift
      shift
      ;;
    -t|--bottoken)
      TOKEN="$2"
      shift
      shift
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") #
      shift
      ;;
  esac
done

echo "installation script started"

apt install docker.io docker-compose -y
docker swarm init

echo "Packages installed"

echo "${RTOKEN}" | docker secret create rtoken -

echo "[api]
id = ${APIID}
hash = ${APIHASH}
[session]
string = ${STRINGSESSION}" | docker secret create string_session -

echo "[token]
token = ${TOKEN}
admin = ${ADMINUSER}" | docker secret create token -

echo "${DATABASEPASS}" | docker secret create db_password -

echo "Secrets created"

docker network create -d overlay --subnet=10.11.0.0/16 --attachable grabber_net

echo "Overlay network created"

docker stack deploy --compose-file stack.yml promograb

echo "Stack deployed"