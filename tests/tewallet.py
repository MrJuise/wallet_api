# from httpx import AsyncClient, ASGITransport
#
# from app.main import app
# import pytest
#
# @pytest.fixture
# async def client():
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
#         yield ac
#
#
# @pytest.mark.asyncio
# async def test_add_wallet(client):
#         response = await client.post("/api/v1/add", json={"balance": 100})
#         data = response.json()
#         assert response.status_code == 201
#
#         print("balalalalalalalnce: ", data["balance"])
#         assert data["balance"] == 100
#
# @pytest.mark.asyncio
# async def test_get_wallet(client):
#     wallet = await client.post("/api/v1/get", json={"balance": 100})
#     data = wallet.json()
#     uuid_wallet = data["uuid"]
#
#     response = await client.get("/api/v1/get", json={"uuid": uuid_wallet})
#
#

