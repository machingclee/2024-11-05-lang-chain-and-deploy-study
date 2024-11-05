FROM public.ecr.aws/lambda/python:3.10
WORKDIR /var/task
COPY . .
ENV PYTHONPATH=/var/task

RUN yum install -y \
    gcc \
    gcc-c++ 
RUN pip install --no-cache-dir -r requirements.txt
RUN yum remove -y gcc gcc-c++ && \
    yum clean all

CMD ["wsgi_handler.lambda_handler"]