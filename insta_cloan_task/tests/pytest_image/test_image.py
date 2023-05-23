from pytest_bdd import scenario, given, when, then
import json, pytest
from flask.testing import FlaskClient
from tests.pytest_image.seed_data_image import SEED_DATA_IMAGE
from tests.pytest_user.seed_data_user import SHARED_SEED_DATA_ACTION
from werkzeug.datastructures import FileStorage


DATA_FILE = (
    "/home/rootz/learning/Rjoisehub/flask/insta_cloan_task/tests/pytest_image/image.feature"
)

@pytest.mark.seed_data(("user", SHARED_SEED_DATA_ACTION["user"]))
@scenario(DATA_FILE, "Post a image")
def test_upload_image(client: FlaskClient, seed):
    """_summary_

    Args:
        client (FlaskClient): _description_
        seed (_type_): _description_
    """

@pytest.mark.seed_data(("user", SHARED_SEED_DATA_ACTION["user"]))
@given("Get img_filename and caption")
def test_select_image(client: FlaskClient, seed):
    file = FileStorage(
        filename="test_image.jpg",
        content_type="image/jpeg",
    )

    caption = "Test caption"

    id = pytest.id_for("ENTITY_IDENTIFIER_1")
    token = pytest.token_for({"id": id})

    response = client.post(
        "/upload_image",
        data={
            "post_image": file,
            "caption": caption,
        },
        content_type="multipart/form-data",
        headers={"Authorization": token},
    )

    assert response.status_code == 200


# @pytest.mark.seed_data(("image_post", SEED_DATA_IMAGE["image_post"]))
# @given("I should see a success message")
# def test_image_success(client: FlaskClient, seed):
#     """verify success message"""

#     user_id = pytest.id_for("ENTITY_IDENTIFIER_1")

#     id = pytest.id_for("ENTITY_IDENTIFIER_2")
#     # token = pytest.token_for(user_id)

#     response = client.get(
#         f"/get_image/{user_id}",
#         content_type="multipart/form-data",
#         # headers={"Authorization": token}
#     )

#     assert response.status_code == 200

#     assert response.json["caption"] == "always on fire"
#     assert (
#         response.json["img_filename"] == f'{pytest.id_for("ENTITY_IDENTIFIER_3")}.jpg'
    # )
