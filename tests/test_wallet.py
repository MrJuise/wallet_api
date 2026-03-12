import asyncio
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.main import app
from app.db.db_session import get_sessionmaker
from app.models.models_wallets import Wallet


@pytest.fixture
def client():
    Session = get_sessionmaker()

    async def clear_db():
        async with Session() as db:
            await db.execute(delete(Wallet))
            await db.commit()

    asyncio.run(clear_db())

    with TestClient(app) as c:
        yield c

    asyncio.run(clear_db())


def create_wallet(balance=1000):
    Session = get_sessionmaker()

    async def _create():
        wallet_uuid = uuid.uuid4()
        async with Session() as db:
            wallet = Wallet(uuid=wallet_uuid, balance=balance)
            db.add(wallet)
            await db.commit()
        return wallet_uuid

    return asyncio.run(_create())


def test_get_balance(client):
    wallet_uuid = create_wallet(1000)

    r = client.get(f"/api/v1/wallets/{wallet_uuid}")

    assert r.status_code == 200
    assert r.json()["balance"] == 1000


def test_deposit_withdraw(client):
    wallet_uuid = create_wallet(1000)

    r1 = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": 500},
    )

    assert r1.status_code == 200
    assert r1.json()["balance"] == 1500

    r2 = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": 300},
    )

    assert r2.status_code == 200
    assert r2.json()["balance"] == 1200


def test_concurrent_withdraw(client):
    wallet_uuid = create_wallet(1000)

    def withdraw():
        return client.post(
            f"/api/v1/wallets/{wallet_uuid}/operation",
            json={"operation_type": "WITHDRAW", "amount": 800},
        )

    r1 = withdraw()
    r2 = withdraw()

    statuses = {r1.status_code, r2.status_code}
    assert statuses == {200, 400}

    balance = client.get(f"/api/v1/wallets/{wallet_uuid}")
    assert balance.json()["balance"] == 200