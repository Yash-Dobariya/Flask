import factory
from pytest_factoryboy import register
from faker import Factory as FakerFactory
from src.user.model import User
from src.image.model import ImagePost

faker = FakerFactory.create()


@register
class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.LazyAttribute(lambda x: str(faker.uuid4))
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    email_id = factory.LazyAttribute(faker.email)
    password = factory.LazyAttribute(faker.password())
    dob = factory.LazyAttribute(lambda x: faker.date_of_birth().strftime('%d-%m-%Y'))
    country = factory.LazyAttribute(lambda x: faker.country())
    bio = factory.LazyAttribute(lambda x: faker.text())


@register
class ImagePostFactory(factory.Factory):
    
    class Meta:
        model = ImagePost
    
    id = factory.LazyAttribute(lambda x: str(faker.uuid4))
    file_name = factory.LazyAttribute(lambda x: faker.file_name(extension='jpg'))
    caption = factory.LazyAttribute(lambda x: faker.sentence(nb_words=6, variable_nb_words=True))
    uploaded_by = factory.LazyAttribute(lambda x: str(faker.uuid4))
    count_like = factory.LazyAttribute(lambda x: faker.int())
    liked_by = factory.LazyAttribute(lambda x: faker.uuid4)
    comment = factory.LazyAttribute(lambda x: faker.sentence())
    