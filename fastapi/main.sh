set -o allexport
source ../.env
POSTGRES_HOST="localhost"
ELASTIC_URL="http://localhost:9200"
ETL_BATCHSIZE=100
REDIS_DSN="redis://localhost:6379"
set +o allexport

python main.py
