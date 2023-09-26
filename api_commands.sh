# DOCKER - Executed commands :

docker image build . -t airfrance_api_image:latest --no-cache
docker container run --network host --name airfrance_api_container --rm airfrance_api_image:latest
docker container ls
docker container ls -a
docker container stop 0b0d6acc8a0f
docker image rm -f airfrance_api_image
docker compose down # Stupprimer tous les dockers
docker-compose up --build # Lancer le docker-compose en supprimant toutes les images

curl -X GET -i http://3.10.117.213:8000/docs

# DOCKER - Information about Dockerfile :
CMD uvicorn api:api --host 0.0.0.0 --port 8000 --reload :\
    --host has been added in order for Uvicorn running in the container not to be restricted to the incoming host IP