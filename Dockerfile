FROM fedora:26

RUN dnf install -y python35 python3-pip python3-virtualenv git npm \
        python3-devel gcc krb5-devel && \
        dnf clean all

WORKDIR /app/

VOLUME ["/app/node_modules/"]

COPY . ./docker/ /app/

RUN ./setup.sh --venv /app/.venv

ENTRYPOINT ["/app/docker/entrypoint.sh", "--venv", "/app/.venv"]
