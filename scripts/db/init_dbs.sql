-- Create the user and database.
CREATE USER :p_user WITH SUPERUSER NOCREATEROLE ENCRYPTED PASSWORD :p_pass;
ALTER USER :p_user CREATEDB;
CREATE DATABASE :p_dbname OWNER :p_user;
