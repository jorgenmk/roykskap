FROM python:3.9-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
