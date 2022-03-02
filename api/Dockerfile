# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#install all required dependencies
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install pip requirements
COPY requirements.txt .
 
RUN python -m pip install -r requirements.txt

WORKDIR /api
COPY . /api
EXPOSE 5000

CMD ["python", "-m" ,"flask","run","--host=0.0.0.0"]

