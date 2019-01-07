FROM python:2
COPY start.sh /start.sh

COPY requirements* ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["/start.sh"]
