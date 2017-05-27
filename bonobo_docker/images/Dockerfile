FROM python:3.6

ARG BONOBO_VERSION

RUN apt-get -y update \
 && apt-get -y install git make vim sudo \
 && pip install -U pip wheel virtualenv \
 && useradd -m bonobo

ENV TINI_VERSION v0.14.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /sbin/tini

RUN echo "bonobo (== ${BONOBO_VERSION})" > /home/bonobo/requirements.txt \
 && cd /home/bonobo \
 && chmod +x /sbin/tini \
 && sudo -u bonobo virtualenv . \
 && sudo -u bonobo bin/pip install -r requirements.txt \
 && (echo 'export PS1="🐵  \w "'; echo '. /home/bonobo/bin/activate'; echo 'alias l="ls -lsah"') >> /home/bonobo/.bashrc

ADD ./entrypoint.sh /usr/local/bin/

WORKDIR /home/bonobo

ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/entrypoint.sh"]
