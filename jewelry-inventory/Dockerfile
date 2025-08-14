FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    libapache2-mod-wsgi-py3 \
    sqlite3 \
    && pip install flask \
    && a2enmod wsgi \
    && apt-get clean

COPY apache.conf /etc/apache2/sites-available/000-default.conf

COPY . /var/www/flask_app

WORKDIR /var/www/flask_app

# Ensure templates and database directories exist and have correct permissions
RUN mkdir -p /var/www/flask_app/templates \
    && mkdir -p /var/www/flask_app \
    && chown -R www-data:www-data /var/www/flask_app \
    && chmod -R 755 /var/www/flask_app \
    && ls -l /var/www/flask_app/templates || echo "Templates directory not found"

# EXPOSE 80    

CMD ["apache2ctl", "-D", "FOREGROUND"]

