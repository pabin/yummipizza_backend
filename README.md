# The Yummi Pizza Backend

### `Clone Repository`

git clone https://github.com/pabin/yummipizza <br />
Clones the backend code to you computer

### `Create Virtual Env`

virtualenv -p python3 env <br />
Creates a virtual invironment to `install` required packages

### `Activate Virtual Env`

source env/bin/activate <br />
Activates the `virtual environment`, so you can install required<br />
packages on the virtual environment

### `Install Packages`

pip install -r requirements.txt  <br />
Installs the packages listed in requirements.txt file

### `Project Pre-Setting`

cd yummipizza <br />
python manage.py migrate <br />
python manage.py loaddata Discounts <br />
python manage.py loaddata ItemInventory <br />
python manage.py runserver <br />

Move to the project root folder. Migrate to create the database models <br />
then create default data like discounts and item inventory from fixtures.


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


### `Available Features`

User Account  <br />
Item Inventory <br />
Shopping Cart Item <br />
Shopping Cart <br />
Orders and Order Items <br />
Reviews and Ratings <br />
