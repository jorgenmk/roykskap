FROM python:3.9-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
RUN ls
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]