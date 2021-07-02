FROM python:3
RUN pip install bs4 requests

CMD [ "python", "/root/app/philippine.py" ]
