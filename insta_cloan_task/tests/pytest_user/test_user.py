import json, pytest
from flask.testing import FlaskClient
from tests.pytest_user.seed_data_user import SHARED_SEED_DATA_ACTION


def test_sign_up(client: FlaskClient):
    response = client.post(
        "/sign_up",
        data=json.dumps(
            {
                "id": pytest.id_for("ENTITY_IDENTIFIER_1"),
                "first_name": "yash",
                "last_name": "dobariya",
                "email_id": "yash@gmail.com",
                "password": "123",
                "dob": "23-02-2003",
                "country": "india",
                "bio": "i am good",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 201

    assert response.json["id"] == pytest.id_for("ENTITY_IDENTIFIER_1")
    assert response.json["first_name"] == "yash"
    assert response.json["last_name"] == "dobariya"
    assert response.json["email_id"] == "yash@gmail.com"
    assert response.json["country"] == "india"
    assert response.json["bio"] == "i am good"


@pytest.mark.seed_data(("user", SHARED_SEED_DATA_ACTION["user"]))
def test_login(client: FlaskClient, seed):
    response = client.post(
        "/sign_in",
        data=json.dumps({"email_id": "yash@gmail.com", "password": "123"}),
        content_type="application/json",
    )

    assert response.status_code == 200


@pytest.mark.seed_data(("user", SHARED_SEED_DATA_ACTION["user"]))
def test_get_all_user(client: FlaskClient, seed):
    response = client.get(
        "/get_all",
        content_type="application/json",
    )

    assert response.status_code == 200


@pytest.mark.seed_data(("user", SHARED_SEED_DATA_ACTION["user"]))
def test_get_particular_user(client: FlaskClient, seed):
    id = pytest.id_for("ENTITY_IDENTIFIER_1")
    response = client.get(f"/get/{id}", content_type="application/json")

    assert response.status_code == 200

    assert response.json["first_name"] == "yash"
    assert response.json["last_name"] == "dobariya"
    assert response.json["email_id"] == "yash@gmail.com"
    assert response.json["country"] == "india"


@pytest.mark.seed_data(("user", SHARED_SEED_DATA_ACTION["user"]))
def test_update_user(client: FlaskClient, seed):
    id = pytest.id_for("ENTITY_IDENTIFIER_1")
    token = pytest.token_for({"id": id})

    response = client.put(
        f"/update/{id}",
        data=json.dumps({"country": "canada"}),
        headers={"Authorization": token},
        content_type="application/json",
    )
    assert response.status_code == 200

    assert (
        response.json["message"]
        == f"{pytest.id_for('ENTITY_IDENTIFIER_1')} update successfully"
    )


@pytest.mark.seed_data(("user", SHARED_SEED_DATA_ACTION["user"]))
def test_delete_user(client: FlaskClient, seed):
    id = pytest.id_for("ENTITY_IDENTIFIER_1")
    token = pytest.token_for({"id": id})
    response = client.delete(
        f"/delete/{id}",
        headers={"Authorization": token},
        content_type="application/json",
    )

    assert response.status_code == 200

    assert (
        response.json["message"]
        == f"{pytest.id_for('ENTITY_IDENTIFIER_1')} deleted successfully"
    )
