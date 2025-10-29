set -e

docker run --network localstack --rm -it \
  -v "./localstack/.aws:/root/.aws" \
  amazon/aws-cli --endpoint-url=http://localstack:4566 "$@"