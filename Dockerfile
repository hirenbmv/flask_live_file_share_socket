# Fetch the python3 docker image
FROM python:3.12

# Set the working dir
WORKDIR /flask_live_file_share_socket

# Copy only the requirements file first
COPY requirements.txt /flask_live_file_share_socket/

# Command to install python depedencies
RUN pip install -r requirements.txt --no-cache-dir

# copy project to working dir
COPY . /flask_live_file_share_socket
