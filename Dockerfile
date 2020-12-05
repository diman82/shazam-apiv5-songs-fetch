FROM python
WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD main.py logging_config.yaml ./
EXPOSE 80
CMD ["python", "main.py", "/app/mnt/urls.txt"]