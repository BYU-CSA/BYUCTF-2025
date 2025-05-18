# Use a base Python image
FROM python:3.11

# create unpriv user
RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

# Copy application files
COPY main.py .
COPY DAOs/ DAOs/
COPY Models/ Models/
COPY templates/ templates/
COPY static/ static/

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# set perms
RUN chown -R root:ctf /ctf 
RUN chmod -R 750 /ctf

# Run the database setup script first, then start main.py
USER ctf
CMD ["python3", "main.py"]
EXPOSE 1337