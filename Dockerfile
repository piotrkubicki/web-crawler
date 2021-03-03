FROM python:3.8

WORKDIR /app

COPY main.py setup.py config.py Makefile logging.yaml ./
COPY tests ./tests
COPY tmp ./tmp
COPY site_map ./site_map
RUN make install-dev
ENTRYPOINT [ "python", "main.py"]
