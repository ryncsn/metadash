FROM fedora:26

RUN dnf install -y python35 python3-pip git npm && \
    dnf clean all

WORKDIR /var/www/metadash

COPY . docker/entrypoint.sh docker/uwsgi.ini /var/www/metadash/

RUN ./setup.sh

ENTRYPOINT ['entrypoint.sh']
