FROM python:3.9.6
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Get the Real World example app
RUN git clone https://github.com/paltom/hotel-reservations-api /api_src
WORKDIR /api_src
RUN pip install -r requirements.txt
EXPOSE 8000
WORKDIR /api_src/hra
CMD python manage.py makemigrations &&\
    python manage.py migrate &&\
    python manage.py runserver 0.0.0.0:8000
