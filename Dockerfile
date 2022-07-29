FROM ubuntu:22.04 
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update 
RUN apt-get install -qq qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools
RUN apt-get install -qq python3-pip
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
COPY . /
RUN apt-get install -qq tesseract-ocr-jpn
CMD ["python3", "/main.py"] 