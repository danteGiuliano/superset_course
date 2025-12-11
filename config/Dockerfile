FROM apache/superset:6.0.0rc1

USER root

# Dependencias del sistema , esta es una configuracion personal , donde testeo las ultimas novedades.
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

RUN uv pip install --no-cache-dir gevent

ENV CHROME_PATH=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV CHROME_BIN=/usr/bin/chromium
ENV DISPLAY=:99

RUN chmod 755 /usr/bin/chromium && \
    chmod 755 /usr/bin/chromedriver && \
    mkdir -p /home/superset/.config/chromium && \
    mkdir -p /tmp/.X11-unix && \
    chmod 1777 /tmp/.X11-unix && \
    chown -R superset:superset /home/superset

RUN uv pip install --no-cache-dir \
    psycopg2-binary \
    mysqlclient \
    sshtunnel \
    pillow \
    flask_cors \
    selenium

RUN uv pip install --no-cache-dir prophet


RUN uv pip install --no-cache-dir "shillelagh[gsheetsapi]"

RUN chromium --version && chromedriver --version


#Automatizacion de creacion de usuario.
COPY ./superset-init.sh /superset-init.sh
RUN chmod +x /superset-init.sh

USER superset

# ENTRYPOINT ["/superset-init.sh"]