FROM node:20-alpine

# Add a non-root user (www)
RUN adduser -D www

# Install system packages
RUN apk add --update --no-cache supervisor nginx python3 py3-pip uwsgi uwsgi-python3


# Create application directory
RUN mkdir -p /app
WORKDIR /app

# Copy backend code and requirements from challenge/backend into /app/backend
COPY challenge  .

# Upgrade pip and install backend dependencies using a virtual environment
RUN python3 -m venv venv
RUN /app/venv/bin/pip install --upgrade pip
RUN . /app/venv/bin/activate && pip install -r requirements.txt

# Return to the app root
WORKDIR /app

# Fix permissions for security
RUN chown -R www:www /app
RUN chown -R www:www /var/lib/nginx

# Copy Supervisord and Nginx configuration files
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf

# Expose the port (nginx is configured to serve on port 1337)
EXPOSE 1337

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Start supervisord (which will launch Gunicorn for Flask, Node for frontend, and Nginx)
ENTRYPOINT ["supervisord", "-c", "/etc/supervisord.conf"]
