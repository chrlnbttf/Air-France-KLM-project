
docker image build . -t airfrance_db_image:latest
docker container run --network host --name airfrance_db_container --rm airfrance_db_image:latest