FROM python:3.11-slim-bullseye

# install pip dependency
RUN  pip install pyyaml \
                 line_notify \
                 requests \
                 beautifulsoup4 \
                 pandas \
                 geopandas \
                 matplotlib

COPY secret.yaml secret.yaml
COPY config.yaml config.yaml
COPY assets/*    assets/
COPY src/*       src/

WORKDIR src/

CMD ["python", "task_2.py"]
