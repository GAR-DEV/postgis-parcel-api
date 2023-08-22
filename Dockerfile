FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip 


RUN apt-get update \
    && apt-get install -y libpq-dev

WORKDIR /new-parcel-api

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r /new-parcel-api/requirements.txt && \
    rm -rf /root/.cache

COPY . .


CMD ["waitress-serve", "--port=80", "--call", "app:create_app"]

# Start the Flask app
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"] 
#remove --post=80 for local run