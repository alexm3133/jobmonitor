# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /PROJECTEJOANJORDI

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Command to run on container start
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]
