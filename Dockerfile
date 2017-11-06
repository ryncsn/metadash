FROM fedora:26

RUN dnf install -y python35 python3-pip python3-virtualenv git npm && \
    dnf clean all

WORKDIR /app/

VOLUME ["/app/node_modules/", "/app/metadash/plugins/", "/app/.venv"]

COPY . /app/

RUN ./setup.sh --venv /app/.venv

ENTRYPOINT ["/app/docker/entrypoint.sh --venv /app/.venv"]
