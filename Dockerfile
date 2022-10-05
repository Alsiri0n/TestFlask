FROM centos:latest
ENV FLASKP='5050'
ENV FLASKH=0.0.0.0
RUN cd /etc/yum.repos.d/
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
RUN yum install net-tools -y
RUN yum install httpd -y
RUN yum install python3 -y
RUN echo $FLASKP
RUN echo $PATH
COPY requirements.txt /home
RUN pip3 install -r /home/requirements.txt
COPY WEB_APP My_App
WORKDIR My_App
ENTRYPOINT ["python3", "app.py"]
EXPOSE 3000 5050