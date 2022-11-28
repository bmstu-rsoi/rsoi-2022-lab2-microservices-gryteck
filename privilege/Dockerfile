FROM python:3.9.6
EXPOSE 8050
WORKDIR /main
COPY main.py /main
COPY privilege_db.py /main
COPY requirements.txt /main/requirements.txt
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]