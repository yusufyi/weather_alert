import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload =dict(
        username = 'TestUser',
        email='test@test.com',
        password='test_passowrd',
        )

    response = client.post("/users_create/",payload)

    data = response.data

    assert data["username"] == payload['username']
    assert data["email"] == payload['email']
    assert 'password' not in data


@pytest.mark.django_db
def test_auth_token():
    payload =dict(
        username = 'TestUser',
        email='test@test.com',
        password='test_passowrd',
        )
    
    client.post("/users_create/",payload)
    
    response =client.post("/api-token-auth/",payload)
    
    data = response.data
    
    assert 'token' in data
    assert response.status_code == 200



@pytest.mark.django_db
def test_login_iser_fail():
    response = client.post("/api-token-auth/",dict(username="test",password='WrongPass'))
    assert response.status_code == 400


@pytest.mark.django_db
def test_list_user_with():
    payload =dict(
        username = 'TestUser',
        email='test@test.com',
        password='test_passowrd',
        )
    
    client.post("/users_create/",payload)
    
    response =client.post("/api-token-auth/",payload)
    
    data = response.data['token']
  
    client.credentials(HTTP_AUTHORIZATION='Token ' + data)

    r =client.get("/users/")
    d = r.data
    assert r.status_code == 200
    print (d)
    assert d[0]['user']["username"] == "TestUser"
    assert d[0]['user']["email"] == "test@test.com"


@pytest.mark.django_db
def test_list_user_wrong_token():

    token = 'WrongToken'
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    response =client.get("/users/")
    data = response.data
    assert response.status_code == 401
    assert data["detail"] == "Invalid token."
    
