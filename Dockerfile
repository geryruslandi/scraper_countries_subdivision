FROM python:3
RUN pip install bs4 requests

COPY . .
CMD [ "python", "./indonesia.py" ]
