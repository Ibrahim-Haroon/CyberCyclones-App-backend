FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV TZ=America/New_York

WORKDIR /cybercyclones

RUN apt-get update && \
    apt-get install -y \
        portaudio19-dev \
        flac \
        ffmpeg

COPY requirements_pip.txt .

RUN pip install -r requirements_pip.txt

COPY . .

EXPOSE 8000

CMD bash -c "python manage.py makemigrations src && \
             python manage.py migrate src && \
             python manage.py migrate && \
             python manage.py runserver 0.0.0.0:8000"