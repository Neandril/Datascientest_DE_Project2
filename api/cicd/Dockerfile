# Base Image
FROM python:3.9.11

# Install dependencies
RUN pip install --no-cache-dir fastapi requests

# Set the Working Directory
WORKDIR /api/ci-cd

# Add the script
ADD api_ci-cd.py api_ci-cd.py
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh

# Expose this port
EXPOSE 8000

# Set Env Variable LOG to 1
ENV LOG 1

# Execute the script
# ENTRYPOINT ["python3", "api_ci-cd.py"]
ENTRYPOINT [ "/bin/bash" ]
CMD [ "./wait-for-it.sh", "0.0.0.0:8080", "--timeout=5", "--", "python3", "api_ci-cd.py" ]
