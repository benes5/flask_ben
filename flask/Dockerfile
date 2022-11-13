FROM python:3.7.5

# ARG app_dir=/app/
WORKDIR /app

COPY requrements.txt ./


# ADD requirements.txt $app_dir


RUN pip install --upgrade pip

# 利用するパッケージがかたまるまでコメントアウトしてても良さそう
RUN pip install flask
RUN pip install flask_sqlalchemy
RUN pip install flask_cors
RUN pip install psycopg2

COPY . .

RUN python database.py
EXPOSE 8080
CMD ["python", "server.py"]