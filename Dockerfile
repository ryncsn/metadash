FROM fedora:29
WORKDIR /app/

RUN dnf install -y which python3 nodejs pipenv && dnf clean all

COPY . /app/

ARG RELATIVE_PATH
ENV APP_RELATIVE_PATH=${RELATIVE_PATH}
ENV PATH="/app/bin:${PATH}"

RUN dnf install -y git gcc krb5-devel && \
        ./bin/md-manager setup && \
        dnf remove -y git gcc krb5-devel && \
        dnf clean all

VOLUME ["/app/node_modules/"]
ENTRYPOINT ["bash", "-c", "/app/deploy/entrypoint.sh"]
