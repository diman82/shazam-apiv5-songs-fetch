FROM python
WORKDIR /app
ADD main.py requirements.txt logging_config.yaml ./
RUN pip install -r requirements.txt
EXPOSE 80
ENV NAME world
CMD [“python”, “main.py”, “urls.txt”]