FROM python:3.10.11-slim

RUN ln -fs /usr/share/zoneinfo/Asia/Phnom_Penh /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /var/log/gunicorn/
RUN touch /var/log/gunicorn/access.log
RUN touch /var/log/gunicorn/error.log

EXPOSE 8080
CMD gunicorn --workers=5 --threads=2 --access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log -b 0.0.0.0:8080 run:app && tail -f /var/log/gunicorn/error.log