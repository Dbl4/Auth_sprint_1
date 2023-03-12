set -o allexport
source ../.env
POSTGRES_HOST="127.0.0.1"
ELASTIC_URL="http://127.0.0.1:9200"
ETL_BATCHSIZE=100
set +o allexport

python main.py
