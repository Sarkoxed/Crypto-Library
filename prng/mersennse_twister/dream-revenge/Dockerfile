FROM python:slim AS app
RUN pip install --no-cache-dir pycryptodome
FROM pwn.red/jail
COPY --from=app / /srv
COPY chall.py /srv/app/run
RUN chmod +x /srv/app/run
COPY flag.txt /srv/app/flag.txt
ENV JAIL_MEM=20M JAIL_ENV_NUM=5
