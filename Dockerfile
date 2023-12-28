# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Clone the repository
RUN git clone https://github.com/chhofi/PixelTixel

# Install any needed packages specified in PixelTixel/requirements.txt
RUN pip install --no-cache-dir -r ./PixelTixel/requirements.txt

# Change to the PixelTixel directory and run the script
CMD cd PixelTixel && python pixelflut.py
