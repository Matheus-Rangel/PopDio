FROM python:3.7.2

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ARG postgres_user="postgres"
ENV POSTGRES_USER=$postgres_user

ARG postgres_password="123456"
ENV POSTGRES_PASSWORD=$postgres_password

ARG postgres_db="pop-fibras-dev"
ENV POSTGRES_DB=$postgres_db

ARG postgres_host="postgres"
ENV POSTGRES_HOST=$postgres_host

ARG postgres_port="5432" 
ENV POSTGRES_PORT=$postgres_port

ARG secret_key='_5#y2L"F4Q8z\n\xec]/'
ENV SECRET_KEY=$secret_key

CMD ["python", "app.py"]