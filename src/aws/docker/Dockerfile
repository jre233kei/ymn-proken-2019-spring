FROM lambci/lambda:build-python3.6
ENV LANG C.UTF-8
ENV AWS_DEFAULT_REGION ap-northeast-1

WORKDIR /var/task
ADD . .

RUN /bin/cp -f /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
  pip3 install -r requirements.txt -t /var/task --upgrade && \
  python3 learning.py train-9.lst model.bin 

CMD zip -9 deploy_package.zip lambda_function.py model.bin && \
  zip -r9 deploy_package.zip *
