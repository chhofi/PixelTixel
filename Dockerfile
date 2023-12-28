# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Clone the repository or copy the script
# For example, cloning a repository:
RUN git clone https://github.com/chhofi/PixelTixel

# Set the command to run your script
CMD ["python", "./pixelflut.py"]

