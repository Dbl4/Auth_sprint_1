curl -XPOST http://127.0.0.1:9200/genres/_doc/112B0D92-09FF-46CF-97D6-D30F538652EE -H 'Content-Type: application/json' -d'
{
    "id": "112B0D92-09FF-46CF-97D6-D30F538652EE",
    "name": "Action"
}'
curl -XPOST http://127.0.0.1:9200/genres/_doc/2838E473-F646-4CE0-B5CF-17DF13EB9117 -H 'Content-Type: application/json' -d'
{
    "id": "2838E473-F646-4CE0-B5CF-17DF13EB9117",
    "name": "Drama"
}'
curl -XPOST http://127.0.0.1:9200/genres/_doc/C0D5635D-7C9F-4C7C-B785-0A926CCE3BD4 -H 'Content-Type: application/json' -d'
{
    "id": "C0D5635D-7C9F-4C7C-B785-0A926CCE3BD4",
    "name": "Dramedy"
}'

curl -XPOST http://127.0.0.1:9200/persons/_doc/DA271596-F7C8-40D5-8C22-9FB0C9E6DAC6 -H 'Content-Type: application/json' -d'
{
    "uuid": "DA271596-F7C8-40D5-8C22-9FB0C9E6DAC6",
    "full_name": "Karen Cornwell",
    "role": "actor",
    "film_ids": ["3E21BF14-AE47-40F0-B71D-459EC61EB4F8"]
}'

curl -XPOST http://127.0.0.1:9200/persons/_doc/A18CBB60-F0EC-4A87-AD37-3E48D8CF3735 -H 'Content-Type: application/json' -d'
{
    "uuid": "A18CBB60-F0EC-4A87-AD37-3E48D8CF3735",
    "full_name": "Robbie Daymond",
    "role": "writer",
    "film_ids": ["3F1DCB88-EBBA-4B45-ACB5-E6DDC723B632"]
}'

curl -XPOST http://127.0.0.1:9200/persons/_doc/B7857A41-C497-417D-90E5-0A9BA009EE12 -H 'Content-Type: application/json' -d'
{
    "uuid": "B7857A41-C497-417D-90E5-0A9BA009EE12",
    "full_name": "Christopher Miranda",
    "role": "actor",
    "film_ids": ["3FF6803B-D276-42DE-8CE8-2811123AD233"]
}'
