FROM python:3.10.12

 WORKDIR /app
 
 COPY requirements.txt .
 RUN pip install python-telegram-bot --upgrade
 RUN pip install -r requirements.txt --upgrade

 COPY . .


 CMD ["python", "./main/main.py"]