from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def tets_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codewithsai'
    assert response.json()['email'] == 'codewithsai@gmail.com'
    assert response.json()['first_name'] == 'sai'
    assert response.json()['last_name'] == 'teja'

def teat_change_password(test_user):
    response = client.put("/user/password", json = {"password": "test123", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_invalid_password(test_user):
    response = client.put("/user/password", json={"password": "wrong", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Invalid password'}

def test_phone_number_success(test_user):
    response = client.put("/user/phonenumber/1234567899")
    assert response.status_code == status.HTTP_204_NO_CONTENT