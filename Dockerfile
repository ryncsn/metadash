FROM fedora:29
WORKDIR /app/

RUN dnf install -y python3 nodejs pipenv && dnf clean all

COPY . /app/

RUN dnf install -y gcc python3-devel krb5-devel && \
        ./bin/md-manager setup && \
        dnf remove -y gcc python3-devel krb5-devel && \
        dnf clean all

VOLUME ["/app/node_modules/"]
ENTRYPOINT ["bash", "-c", "/app/deploy/entrypoint.sh"]
