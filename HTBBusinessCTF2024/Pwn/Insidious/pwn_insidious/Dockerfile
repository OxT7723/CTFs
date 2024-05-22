FROM ubuntu:22.04

RUN apt-get update --fix-missing && apt-get -y upgrade
RUN apt-get install -y socat

RUN useradd -m ctf -u 1000

WORKDIR /home/ctf
COPY challenge .
RUN chmod u+s ./insidious && chmod 0400 ./flag.txt

USER ctf

EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./insidious"]
