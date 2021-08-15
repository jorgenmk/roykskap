FROM python:3.9-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY app.py /app
RUN ls
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0"]