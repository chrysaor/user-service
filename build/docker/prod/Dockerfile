# Pull official base image
FROM ubuntu:18.04

# Set work directory
WORKDIR /home/user-service

# Install python 3.7.7
RUN apt-get update
RUN apt-get install -y python3.7 python3-pip vim
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN update-alternatives --set python /usr/bin/python3.7
RUN python -m pip install --upgrade pip

# Install dependencies
COPY ./requirements.txt /home/user-service/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Copy project directory
COPY ./app /home/user-service/app

# Copy scripts directory
COPY ./scripts/start_server.sh /home/user-service/scripts/start_server.sh

# Set environment variables
ENV USER_SERVICE_DIR /home/user-service
ENV FLASK_ENV production

# Expose the flask port
EXPOSE 5000

# Run server
CMD ["sh", "/home/user-service/scripts/start_server.sh"]
