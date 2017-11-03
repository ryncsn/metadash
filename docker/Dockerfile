FROM fedora:26

RUN dnf install -y python35 python3-pip

WORKDIR /var/www/metadash

COPY .. ./
COPY entrypoint.sh /var/www/metadash

RUN ./setup.sh --no-venv

# Copy the modified Nginx conf
COPY uwsgi.ini ./

ENTRYPOINT ['entrypoint.sh']
