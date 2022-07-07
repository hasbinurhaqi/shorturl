
FROM python:3.9-alpine

WORKDIR /services

COPY ./requirements.txt /services/requirements.txt

RUN apk update && apk add --no-cache g++ jpeg-dev zlib-dev libjpeg make linux-headers cmake unzip build-base swig sqlite
#RUN apk update && apk add --no-cache g++ jpeg-dev zlib-dev libjpeg make linux-headers cmake unzip build-base tesseract-ocr tesseract-ocr-data-ind 

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /services/requirements.txt

COPY ./app /services/app

RUN mkdir -p /services/app/temp

RUN chmod -R 777 /services/app/temp

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]


# FROM python:3.9-alpine

# WORKDIR /services

# COPY ./requirements.txt /services/requirements.txt

# RUN apk update && apk add --no-cache g++ jpeg-dev zlib-dev libjpeg make tesseract-ocr tesseract-ocr-data-deu 

# RUN pip install --no-cache-dir --upgrade -r /services/requirements.txt

# COPY ./app /services/app

# RUN mkdir -p /services/app/temp

# RUN chmod -R 777 /services/app/temp

# CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]


