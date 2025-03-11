FROM php:8.1-apache

COPY src/ /var/www/html/
COPY flag.txt /flag.txt

RUN mkdir -p /var/www/html/uploads && \
    chown -R www-data:www-data /var/www/html/uploads && \
    chmod -R 755 /var/www/html/uploads

COPY apache-config.conf /etc/apache2/sites-available/000-default.conf

RUN echo "disable_functions = exec,system,shell_exec,passthru,popen,proc_open" > /usr/local/etc/php/php.ini

EXPOSE 8080

CMD ["apache2-foreground"]
