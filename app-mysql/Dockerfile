FROM mysql:9.2

EXPOSE 3306

ARG MYSQL_DATABASE
ARG MYSQL_ROOT_PASSWORD

ENV MYSQL_DATABASE=$MYSQL_DATABASE
ENV MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD

COPY ./setup_db.sql /etc/mysql/

#RUN sed -i 's/MYSQL_DATABASE/'${MYSQL_DATABASE}'/g' /etc/mysql/setup_db.sql
RUN cp /etc/mysql/setup_db.sql /docker-entrypoint-initdb.d

HEALTHCHECK --interval=10s --timeout=10s \  
  CMD mysql -p${MYSQL_ROOT_PASSWORD} -e "SHOW DATABASES;" || exit 1

