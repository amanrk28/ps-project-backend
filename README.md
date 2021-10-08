# ![alt text](https://res.cloudinary.com/retailr/image/upload/v1632934376/products/logoMain_wdwznx.png)

Retailr is made to help local shopkeepers expand their customer base to more than just a locality.

## Basic Scenario

Any local store owner can upload their products and its details on this platform and people can come here to purchase these products like an e-commerce app. After customer makes a puchase, we take care of payments, store pickup and doorstep delivery with minimal service charges based only on the profit gained by said store owner.

### Hosted on Heroku & [Netlify](https://retailr.netlify.app/)

## Tech Stack

- ReactJS
- Django (Rest Framework)
- Docker
- PostgreSQL

## Installation
Get the following tools installed on your local machine:
- [Docker](https://www.docker.com/get-started)
- [pgAdmin](https://www.pgadmin.org/)


## Database Setup

Build and start up db service:
```
make db
```
- Open pgAdmin4
- Right click on Servers => Create => Server...
- Give a name (eg.: local) and fill `localhost` in Host name under Connection tab
- Username: postgres
- Password: postgres
- Save 
- Get a recent DB dump from maintainers and restore DB 
