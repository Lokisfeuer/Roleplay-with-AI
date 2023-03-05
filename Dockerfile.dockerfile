# Dockerfile, Image, Container
# Container with python version 3.10
FROM python:latest

#Labels as key value pair
# LABEL Maintainer="roushan.me17"

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
# WORKDIR /usr/app/src

# Add python file and directory
ADD main.py .

# upgrade pip and install pip packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy && \
    pip install --no-cache-dir openai && \
    pip install --no-cache-dir random && \
    pip install --no-cache-dir os && \
    pip install --no-cache-dir json && \
    pip install --no-cache-dir jsonlines && \
    pip install --no-cache-dir discord && \
    pip install --no-cache-dir datetime && \
    pip install --no-cache-dir math
    # Note: we had to merge the two "pip install" package lists here, otherwise
    # the last "pip install" command in the OP may break dependency resolution...

#to COPY the remote file at working directory in container
# COPY test.py ./
# Now the structure looks like this '/usr/app/src/test.py'

# run python program
CMD ["python", "main.py"]


