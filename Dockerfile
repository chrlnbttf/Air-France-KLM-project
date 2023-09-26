FROM mongo:latest
RUN apt-get update && apt-get install python3-pip -y
RUN pip install pandas
RUN pip install pymongo
RUN pip install requests
ADD upload.py upload.py
ADD airfrance_20230921.json airfrance_20230921.json
ADD airfrance_20230922.json airfrance_20230922.json
ADD airfrance_20230923.json airfrance_20230923.json
ADD airfrance_20230924.json airfrance_20230924.json
ADD airfrance_20230925.json airfrance_20230925.json
EXPOSE 27017
CMD python3 upload.py


