FROM python:3-alpine
MAINTAINER chris elliott <ctelliott@gmail.com>

# install dependencies
ADD ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# add password
ADD ./src /opt/src
RUN chmod +x /opt/src/*.py

CMD ["/opt/src/app.py"]
