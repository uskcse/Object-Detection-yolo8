FROM python:3.11.7-alpine3.17
COPY ./ ./app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD python ./app.py