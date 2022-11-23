FROM python:3.10.4
EXPOSE 8060
WORKDIR /main
COPY main.py /main
COPY flight_db.py /main
COPY requirements.txt /main/requirements.txt
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]