# crypto_price_alert

# Objectives

price alert application that triggers an email when the user’s target price is achieved. it will have endpoints to create alter and that recurcivly checks with https://api.coingecko.com/ for current price and if price match then send notification.

## Stack :
    Djongo/python.
    Mysqldb.
    Redis
    JWT

## Data Model:

```STATUS_CHOICE = [('created', 'created'), ('disabled', "disabled")]```

```json
{
  "coin_id": "",
  "alert_name": "",
  "alert_price": "",
  "status": "created",
  "createdAt": "",
  "createdBy": ""
}
   ```

<!-- TOC -->
    coin_id: Required and same as in coingecko.
    alert_name:  Required 
    alert_price : Required
    status: Required and from STATUS_CHOICE
<!-- TOC -->

## Low level spec:

| Operation                                                                    | Note |
|------------------------------------------------------------------------------|------|
| SignUp user                                   |  Store user information in the database.    |
| Login user                                   |  Login with username and password it will return JWT token.    |
| Create alert                                  | Create alerts , this will required to pass token to authenticate .    |
| Fetch alert                                  | This will fetch all alters of user, it also required token to authenticate. it usage cache it first get data from database and then from redis.   |
| Edit alert                                  | Edit alters of provided id  |
| Delete alert                                  | delete alerts with provided id  |

## API Details:
<!-- TOC -->

## 2. Authentication Request:
    Request Type: POST 
    URL : http://127.0.0.1:8000/signup
    Payload :{
                "username": "admin1",
                "password": "admin@123",
                "email": "admin@test.com"
            }

    Response Status : 201
    Respnse Body : {
                      "id": 1,
                      "username": "admin1",
                      "password": "admin@123",
                      "email": "admin@test.com"
                    }


## 2. Login Request:
    Request Type: POST 
    URL : http://127.0.0.1:8000/login
    Payload :
               {
                    "username" : "",
                    "password" : ""
                }

    Response Status : 200
    Respnse Body : {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzA4MTUyMjAzLCJpYXQiOjE3MDgxNDg2MDN9.UTzb-EJd9cJKho-AR8LBOWy7g7BgV_E6ED-xSt0iLVU",
                    "user": {
                      "id": 1,
                      "username": "admin1",
                      "password": "pbkdf2_sha256$390000$QS6bvfb6fmhKk9H8UltpP1$t6QWKdNYbwZa320rsLpl35Q/A4NQv2oYTlGv31FFmiQ=",
                      "email": "admin@test.com"
                    }
                  }



## 3. Alert Add Request:
    Request Type: POST 
    Authorization: Bearer <token>
    URL : http://127.0.0.1:8000/alerts/create/
    Payload :
               {
                  "coin_id": "bitcoin",
                  "alert_name": "bitcoint_alert",
                  "alert_price": "51621",
                  "status": "created"
                }

    Response Status : 201
    Respnse Body : {
                    "id": 1,
                    "coin_id": "bitcoin",
                    "alert_name": "bitcoint_alert",
                    "alert_price": "51621",
                    "status": "created",
                    "createdBy": 1
                  }

## 4. Alert fetch all:
    Request Type: GET 
    Authorization: Bearer <token>
    URL : http://127.0.0.1:8000/alerts/?page=0&elements=10
    Response Status : 200
    Respnse Body : [{
                    "id": 1,
                    "coin_id": "bitcoin",
                    "alert_name": "bitcoint_alert",
                    "alert_price": "51621",
                    "status": "created",
                    "createdBy": 1
                  }]
   <!-- TOC -->
        page: Page Number.
        elements:  No of Elements in Page.
    <!-- TOC -->
                  
## 5. Alert fetch all with pagination:
    Request Type: GET 
    Authorization: Bearer <token>
    URL : http://127.0.0.1:8000/alerts/?page=0&elements=10&status=created
    Response Status: 200
    Respnse Body : [{
                    "id": 1,
                    "coin_id": "bitcoin",
                    "alert_name": "bitcoint_alert",
                    "alert_price": "51621",
                    "status": "created",
                    "createdBy": 1
                  }]
    <!-- TOC -->
        page: Page Number.
        elements:  No of Elements in Page.
        status: can send status from STATUS_CHOICE
    <!-- TOC -->



## 6. Alert Detail Request:
    Request Type: GET 
    Authorization: Bearer <token>
    URL : http://127.0.0.1:8000/alerts/1/
    Response Status : 200
    Respnse Body : {
                    "id": 1,
                    "coin_id": "bitcoin",
                    "alert_name": "bitcoint_alert",
                    "alert_price": "51621",
                    "status": "created",
                    "createdBy": 1
                  }
                  
## 7. Alert Edit Request:
    Request Type: PUT 
    Authorization: Bearer <token>
    URL : http://127.0.0.1:8000/alerts/1/
    Payload :
               {
                   "id": 1,
                  "coin_id": "bitcoin",
                  "alert_name": "bitcoint_alert",
                  "alert_price": "51621",
                  "status": "created"
                }

    Response Status : 200
    Respnse Body : {
                    "id": 1,
                    "coin_id": "bitcoin",
                    "alert_name": "bitcoint_alert",
                    "alert_price": "51621",
                    "status": "created",
                    "createdBy": 1
                  }


## 7. Alert Delete Request:
    Request Type: DELETE 
    Authorization: Bearer <token>
    URL : http://127.0.0.1:8000/alerts/1/
    Payload :
    Response Status: 204 No content found

<!-- TOC -->
# Steps to run this Application

## 1. Using docker compose
    Need import project from GitHub https://github.com/gauravkri/crypto_price_alert.git
    cd to project root
    RUN command ```docker compose -f docker-compose.yml up -d```
##2 Using project 
    Prerequisites
        * Mysql
        * Redis
        * python
        
    Need import project from GitHub https://github.com/gauravkri/crypto_price_alert.git
    cd to project root
    pip install -r requirements.txt
    Change Redis URL in project/setting.py
    Change mysql config in project/setting.py
    sh start.sh
<!-- TOC -->
    
