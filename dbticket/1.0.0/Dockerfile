FROM python:3.8-slim-bullseye

LABEL maintainer "yun.wang424@hotmail.com"

RUN echo "deb http://deb.debian.org/debian/ bullseye main contrib non-free" >> /etc/apt/sources.list && \
echo "deb-src http://deb.debian.org/debian/ bullseye main contrib non-free" >> /etc/apt/sources.list && \
echo "deb http://deb.debian.org/debian/ bullseye-updates main contrib non-free" >> /etc/apt/sources.list && \
echo "deb-src http://deb.debian.org/debian/ bullseye-updates main contrib non-free" >> /etc/apt/sources.list && \
echo "deb http://security.debian.org/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list && \
echo "deb-src http://security.debian.org/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update && apt-get -yq dist-upgrade && \
  apt-get install -yq  git && \ 
  apt-get clean && rm -rf /var/lib/apt/lists/* 

RUN git clone https://github.com/fulaibaowang/DB_OEBB_ticket.git

RUN pip3 install pdfplumber && python -c "import pdfplumber"
RUN pip3 install pandas && python -c "import pandas"
RUN pip3 install openpyxl && python -c "import openpyxl"
