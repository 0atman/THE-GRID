FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN pip install requests
RUN pip install ipdb
RUN pip install blessings
RUN pip install prompt-toolkit
RUN pip install pygments
RUN pip install fn
RUN pip install webcolors
RUN pip install ply==3.8
RUN pip install ptpython
RUN pip install mypy-lang==0.3.1
RUN pip install flask-restful
RUN pip install Click
RUN pip install tortilla

ADD . /code/
