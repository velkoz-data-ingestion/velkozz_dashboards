FROM python

ENV PYTHONUNBUFFERED 1

COPY . /home/app/ontario_dash_app
WORKDIR /home/app/ontario_dash_app

# Running all of the python install components:
RUN pip install --no-cache-dir -r requirements.txt

# Executing Dash application:
CMD ["python", "index.py"]  
EXPOSE 8010