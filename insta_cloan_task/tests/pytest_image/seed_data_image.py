import pytest

SEED_DATA_IMAGE = {
    "image_post":[
        {
            "id" : pytest.id_for('ENTITY_IDENTIFIER_2'),
            "img_filename": f'{pytest.id_for("ENTITY_IDENTIFIER_3")}.jpg',
            "caption": "always on fire",
            "uploaded_by": pytest.id_for('ENTITY_IDENTIFIER_1'),
        },
    ],
}
