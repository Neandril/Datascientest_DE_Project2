# Base Image
FROM python:3.9.11

# Set the Working Directory
WORKDIR /home/api

# Add necessary files
ADD main.py funcs.py classes.py preds.py ./code/
ADD requirements.txt ./
ADD /pkl/DataForML.pkl /pkl/Final_DT_Model.pkl /pkl/MinMaxScaler.pkl /pkl/All_Models.pkl ./pkl/

# Install requirements
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the port 8000
EXPOSE 8000

# Changing the Workdir for the main code of the api
# WORKDIR /home/api/code

CMD [ "uvicorn", "--app-dir=./code", "main:api", "--reload", "--host",  "0.0.0.0" ]

