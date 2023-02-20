FROM python:3.11-slim-bullseye

# install pip dependency
RUN  pip install pyyaml \
                 line_notify \
                 requests \
                 beautifulsoup4 \
                 pandas \
                 pandasql \
                 geopandas \
                 matplotlib \
                 psycopg2-binary

COPY secret.yaml secret.yaml
COPY config.yaml config.yaml
COPY assets/*    assets/
COPY src/*       src/

WORKDIR src/

CMD ["python", "task_3.py"]
