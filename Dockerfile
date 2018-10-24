FROM fedora:28
WORKDIR /app/

COPY . /app/
RUN dnf install -y python3 python3-pip python3-virtualenv pipenv which \
        git npm python3-devel gcc krb5-devel && \
    ./bin/md-manager setup && \
    dnf remove -y npm gcc krb5-devel && \
    dnf clean all

VOLUME ["/app/node_modules/"]
ENTRYPOINT ["bash", "-c", "/app/docker/entrypoint.sh"]
