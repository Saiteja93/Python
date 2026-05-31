import pytest
from fastapi.testclient import TestClient
import sys
import os
from unittest.mock import patch, MagicMock

#Adding parent directory to path so we can import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

client = TestClient(app)

#Health check

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()['status'] == "Trading API is online"


#----------------------------------------
#POST all trades
#-----------------------------------------

#Data should passed
@patch("routes.trades.producer")
def test_ceate_trade_success(mock_producer):

    mock_producer.send.return_value = MagicMock()

    response = client.post("/trades/", json={
        "symbol": "APPL",
        "price": 200.00,
        "quantity": 5,
        "side": "buy"
    })

    assert response.status_code == 201
    assert response.json()["status"] == "pending"

#Invalid dise data 
@patch("routes.trades.producer")
def test_create_trade_invalid_side(mock_producer):
    response = client.post("/trades", json={
        "symbol": "APPL",
        "price": 200.00,
        "quantity": 5,
        "side": "hold"
    })
    assert response.status_code == 400

#Negative testing on quantity
@patch("routes.trades.producer")
def test_create_trade_negative_quantity(mock_producer):
    response = client.post("/trades", json={
        "symbol": "APPL",
        "price": 200.00,
        "quantity": -5,
        "side": "buy"
    })

    assert response.status_code == 422

@patch("routes.trades.producer")
def test_create_trade_negative_price(mock_producer):
    response  = client.post("/trades", json={
        "symbol": "APPL",
        "price": -200.00,
        "quantity": 5,
        "side": "buy"
    })
    assert response.status_code == 422

@patch("routes.trades.producer")
def test_create_trade_missing_field(mock_producer):
    response = client.post("/trades/",json={
        "symbol": "APPL",
        "price": 200.00,
        
        "side": "buy"

    })
    assert response.status_code == 422
#----------------------------------------
#GET all trades
#-----------------------------------------
def test_get_all_trades():
    response = client.get("/trades")
    assert response.status_code == 200


# GET trade by invalid symbol
def test_get_trade_invalid_symbol():
    response = client.get("/trades/symbol/symbol")
    assert response.status_code == 404

#GET trade by invalid id
def test_get_trade_invalid_id():
    response = client.get("/trades/id/trade_id")

    assert response.status_code == 404

#----------------------------------------
#DELET trade not found
#-----------------------------------------
def test_delete_trade_not_found():
    response = client.delete("/trades/trade_id")
    assert response.status_code == 404


    