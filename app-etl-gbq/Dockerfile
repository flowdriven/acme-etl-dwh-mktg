FROM python:3.12-bookworm 

WORKDIR /app

ARG SECRET 

ENV SECRET=$SECRET

COPY requirements.txt etl_gbq.py ./  

RUN pip install --no-cache-dir -r requirements.txt 

ENTRYPOINT ["/bin/bash", "-c"]

CMD ["cp /run/secrets/${SECRET} /app && python etl_gbq.py"]

# Override to keep the container running: 
#CMD ["cp /run/secrets/${SECRET} /app && python etl_gbq.py && exec bash"] 