FROM python:3.11-slim-bullseye

# install pip dependency
RUN  pip install \
         pyyaml \
         lxml \
         line_notify

COPY . .

WORKDIR src/

CMD ["python", "task_1.py"]
