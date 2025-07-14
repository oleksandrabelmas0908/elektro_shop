FROM python:3.12-slim

WORKDIR /ElektroShop

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "ElektroShop/manage.py", "runserver", "0.0.0.0:8000"]