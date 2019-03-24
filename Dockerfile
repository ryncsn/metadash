FROM fedora:29
WORKDIR /app/

RUN dnf install -y which python3 nodejs pipenv && dnf clean all

COPY . /app/

RUN dnf install -y git gcc krb5-devel && \
        ./bin/md-manager setup && \
        dnf remove -y git gcc krb5-devel && \
        dnf clean all

ENV PATH="/app/bin:${PATH}"
VOLUME ["/app/node_modules/"]
ENTRYPOINT ["bash", "-c", "/app/deploy/entrypoint.sh"]
