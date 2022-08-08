import random
from typing import List

from faker.providers import BaseProvider

from ...common_factories import fake as fake  # explicit reexport
from .graphql_types import Module


class StoreProvider(BaseProvider):
    def module(self) -> Module:
        return Module(
            id=fake.uuid4(),
            name=fake.word(
                ext_word_list=["article", "cartographie", "stock", "transporteur"]
            ),
            version=fake.word(ext_word_list=["1.0.0", "2.1.0", "3.1.5"]),
            author=fake.name(),
            rating=fake.pyfloat(right_digits=1, positive=True, max_value=5),
            num_installs=fake.pyint(),
            screenshots=[fake.image_url() for _ in range(random.randint(1, 5))],
            description=fake.sentence(),
            graphql_schema=fake.text(),
            # widgets=[get_random_widget() for _ in range(random.randint(1, 5))],
        )

    def modules(self) -> List[Module]:
        return [self.module() for _ in range(random.randint(1, 5))]


fake.add_provider(StoreProvider)
