import faker
import faker_microservice
import strawberry
from faker.providers import BaseProvider

from .settings import FAKER_LOCALE

fake = faker.Faker(locale=FAKER_LOCALE)
fake.add_provider(faker_microservice)


class IdentifierProvider(BaseProvider):
    def id(self) -> strawberry.ID:
        """Returns an alphanumerical database ID"""
        return strawberry.ID(fake.password(special_chars=False, length=12))

    def mnemonic_id(self) -> str:
        """Returns a easily-remembered ID"""
        id = fake.password(special_chars=False, upper_case=False, length=8)
        return f"{fake.word()}-{fake.word()}-{id}"


fake.add_provider(IdentifierProvider)
