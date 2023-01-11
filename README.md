<p align="center">
<br />
<img src="https://github.com/pabin/yummipizza_web/blob/master/src/assets/logo/logo_cropped.png?raw=true" width="350" height="58" center />
</p>

## Project Setup Steps


### Clone Project Repository
```
git clone https://github.com/pabin/yummipizza_backend.git
cd yummipizza_backend
```

### Create and Activate Virtual Environment
```
virtualenv -p python3 ../env
source ../env/bin/activate
```

### Install Packages
```
pip install -r requirements.txt
```

### Postgres Database Setup
```
sudo -u postgres psql;
CREATE USER yummipizza WITH PASSWORD '**************';
ALTER ROLE yummipizza SET client_encoding TO 'utf8';
ALTER ROLE yummipizza SET default_transaction_isolation TO 'read committed';
ALTER ROLE yummipizza SET timezone TO 'UTC';
CREATE DATABASE yummipizzadb;
GRANT ALL PRIVILEGES ON DATABASE yummipizzadb TO yummipizza;
```


### Database migration and load fixtures
```
python manage.py migrate
python manage.py loaddata Discounts
python manage.py loaddata ItemInventory

```

### Create superuser
```
python manage.py createsuperuser
```

### Run Project
```
python manage.py runserver
```


### `Available Features`

* User Account  <br />
* Item Inventory <br />
* Shopping Cart Item <br />
* Shopping Cart <br />
* Orders and Order Items <br />
* Reviews and Ratings <br />

### Screenshots
### Admin Panel
![ScreenShot](https://github.com/pabin/yummipizza_backend/blob/master/assets/sreenshots/yummipizza_be_img1.png?raw=true)
