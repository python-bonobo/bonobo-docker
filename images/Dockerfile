FROM python:3.6

RUN apt-get -y update \
 && apt-get -y install vim sudo git
RUN pip install -U pip wheel virtualenv
RUN useradd -m bonobo

ADD requirements.txt /home/bonobo

RUN cd /home/bonobo \
 && sudo -u bonobo virtualenv . \
 && sudo -u bonobo bin/pip install -r requirements.txt
RUN (echo 'export PS1="🐵  \w "'; echo '. /home/bonobo/bin/activate'; echo 'alias l="ls -lsah"') >> /home/bonobo/.bashrc

WORKDIR /home/bonobo

