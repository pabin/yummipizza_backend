# yummipizza

## System Setup  

* Postgres Setup  
	```
    sudo -u postgres psql;
    CREATE USER yummipizza WITH PASSWORD '**************';
    ALTER ROLE yummipizza SET client_encoding TO 'utf8';
    ALTER ROLE yummipizza SET default_transaction_isolation TO 'read committed';
    ALTER ROLE yummipizza SET timezone TO 'UTC';
	  CREATE DATABASE yummipizzadb;
	  GRANT ALL PRIVILEGES ON DATABASE yummipizzadb TO yummipizza;
    ```
