# Subscription Management System

An API based subscription management system, that is designed to manage plans, subscriptions and viewing Exchange Rates with ExchangeRate-API. A minimal backend application mande with Django Rest Framework (DRF)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/rakin54/subscriptionAPI.git
cd subscriptionAPI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python bookishfool/manage.py makemigrations
python bookishfool/manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python bookishfool/manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python bookishfool/manage.py runserver
```

---

## Endpoints and Expected outcomes:

### Register a new user
`POST http://127.0.0.1:8000/api/register/`
Create a new user
Example: 
```JSON
{
    "username" : "user2",
    "email" : "user2@ex.co",
    "password" : "password"
}
```

**Output and Status Code**
- Successful request will return status `201 Created` with message 
```JSON
{
    "message": "User registered successfully!"
}
```

### Login User
`POST http://127.0.0.1:8000/api/login/`

This will allow user to Login the system. Successful credentials will generate two tokens. 
Example: 
```JSON
{
    "username":"user2",
    "password":"password"
}
```

**Output & Status Code**
- Successful login will return status code `200 OK` and will generate two tokens.
```JSON
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```

*Note: for the endpoints that require authentication, `<access_token>` should be used as `Authorization` Header*

The access token will expire after 5 minutes. So, refresh token is needed for generating a new token.

### Refresh Token:
`POST http://127.0.0.1:8000/api/refresh/`
This will generate a new `<access_token>`. Following is the example:
```JSON
{
  "refresh": "<refresh_token>"
}
```
**Output & Status Code**
- Successfull response will return status code `200 OK` with a new access token.
```JSON
{
    "access": "<access_token>"
}
```


### Creates subscribtion

`POST http://127.0.0.1:8000/api/subscribe/`

Create a subscribtion to a plan of the service. User need to be authenticated.
Sample Input

```JSON
{
    "start_date": "2025-6-30",
    "end_date" : "2025-7-31",
    "status" : "active",
    "plan_id" : "2"
}
```

*To get successful response, authentication header is required.*

`Authorization : Bearer <access_token>`

- Successful post request will return status code `201 Created` with message of the data created.
```JSON
{
    "id": 2,
    "start_date": "2025-06-30",
    "end_date": "2025-07-31",
    "status": "active",
    "user": {
        "id": 3,
        "username": "user2",
        "email": "user2@ex.co"
    },
    "plan": {
        "id": 2,
        "name": "Basic",
        "price": "3.00",
        "duration": 30
    }
}
```
- If authentication credentials not provided, then `401 Unauthorized` and message

```JSON
{
    "detail": "Authentication credentials were not provided."
}
```


Since it's JWT token-based authentication, if Token expires `401 Unauthorized` and message

```JSON
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is expired"
        }
    ]
}
```


### View all Subscribtions
`GET http://127.0.0.1:8000/api/subscriptions/`
List all subscribtions of both past and current of the active logged in user.
This endpoint requires Authorization header like following
`Authorization: Bearer <access_token>`

**Output & Status Codes**
- Successful request will return status code `200 OK` with following information if the user is authenticated.
```JSON
[
    {
        "id": 2,
        "start_date": "2025-06-30",
        "end_date": "2025-07-31",
        "status": "active",
        "user": {
            "id": 3,
            "username": "user2",
            "email": "user2@ex.co"
        },
        "plan": {
            "id": 2,
            "name": "Basic",
            "price": "3.00",
            "duration": 30
        }
    }
]
```

- Unauthenticated users will get status `401 Unauthorized`.


### Exchange Rate Endpoints:
`GET http://127.0.0.1:8000/api/exchange-rate/?base=USD&target=BDT`

Get Currency exchange rate information using `ExchangeRate-API`.

**Output & Status Code**
- Successful Responses get status `200 OK` with following data.

```
{
    "base_currency": "USD",
    "target_currency": "BDT",
    "fetched_at": "Fri, 01 Aug 2025 00:00:02 +0000",
    "rate": 122.3321
}
```

- Missing Parameter, Invalid paramete or other errors, it will return `500 Internal Server Error` with the error message. As example like following:

```
  {
      "error": "'NoneType' object has no attribute 'upper'"
  }
```


- Longer currency code will return `400 Bad Request` with message
```
{
    "error": "Currency codes must be 3 characters long"
}
```






