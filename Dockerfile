FROM Centos:7.2
MAINTRAINER xw "xuwei@shouzhengcredit.com"
run yum -y install python3-dev python3-pip
copy ./requirement.txt /requirement.txt
WORKDIR /
RUN pip3 install -r requirement.txt
COPY . /
ENTRYPOINT ["python3"]
CMD ["manage.py runserver 0.0.0.0:5050"]
