FROM python:3.12-bookworm 

WORKDIR /app

COPY requirements.txt load_db.py ./  

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c"]

CMD ["python load_db.py"]

# Override to keep the container running: 
#CMD ["python load_db.py && exec bash"]
