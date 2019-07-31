# Create python image
FROM python:3

# Set working directory
WORKDIR /usr/src/app

# Copy requirements .txt-file
COPY requirements.txt ./

# Install required python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy files to current working directory
COPY . .

# Run script
CMD [ "python3", "./stock_analysis.py" ]