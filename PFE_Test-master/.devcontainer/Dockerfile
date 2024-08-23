ARG base_image_version
FROM mcr.microsoft.com/devcontainers/python:${base_image_version}

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs
RUN pip install robotframework-browser==18.4.0
RUN npx playwright install-deps
RUN rfbrowser init

# Installez wkhtmltopdf afin de convertir html en pdf 
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Définir la variable d'environnement pour wkhtmltopdf
ENV WKHTMLTOPDF_PATH=/usr/bin/wkhtmltopdf
    
COPY .devcontainer/requirements.txt .
#installer les libraries de fichier requirements
RUN pip install --no-cache-dir -r requirements.txt


