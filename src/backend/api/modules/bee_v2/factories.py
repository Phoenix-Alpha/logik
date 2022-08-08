import random
from typing import List

from faker.providers import BaseProvider

from ...common_factories import fake as fake  # explicit reexport
from .graphql_types import Article, Barcode


class Beev2Provider(BaseProvider):
    def barcode(self) -> Barcode:
        return Barcode(
            id=fake.pyint(),
            account_id=fake.pyint(),
            company_id=fake.pyint(),
            article_id=fake.pyint(),
            name=fake.ean(),
            supplier_name=fake.company(),
            supplier_article_code=fake.word(),
            quantity=fake.pyfloat(positive=True, max_value=10),
            rotation=fake.word(),
            preparation_mode=fake.pyint(),
            flag_double=fake.pyint(),
            created_by=fake.name(),
            modified_by=fake.name(),
        )

    def barcodes(self) -> List[Barcode]:
        return [self.barcode() for _ in range(random.randrange(0, 5))]

    def article(self) -> Article:
        article_id = fake.pyint()
        barcodes = fake.barcodes()
        for b in barcodes:
            b.article_id = article_id
        return Article(
            id=article_id,
            account_id=fake.pyint(),
            company_id=fake.pyint(),
            status=fake.pyint(),
            code=fake.word(),
            name=fake.word(),
            additional_description=fake.sentence(),
            supplier_name=fake.company(),
            length=fake.pyfloat(positive=True, max_value=500),
            width=fake.pyfloat(positive=True, max_value=500),
            height=fake.pyfloat(positive=True, max_value=500),
            base_unit_price=fake.pyfloat(positive=True),
            base_unit_weight=fake.pyfloat(positive=True, max_value=10),
            box_weight=fake.pyfloat(positive=True, max_value=10),
            box_quantity=fake.pyfloat(positive=True, max_value=5),
            base_unit_picking=fake.pybool(),
            box_picking=fake.pybool(),
            base_unit_rotation=fake.word(),
            box_rotation=fake.word(),
            cubing_type=fake.pyint(),
            feature_type_id=fake.pyint(),
            permanent_product=fake.pybool(),
            created_by=fake.name(),
            modified_by=fake.name(),
            tariff_classification=fake.word(),
            family=fake.word(),
            subfamily=fake.word(),
            grouping_id=fake.id(),
            barcodes=barcodes,
        )

    def articles(self, max_items: int = 5) -> List[Article]:
        return [self.article() for _ in range(random.randrange(0, max_items))]


fake.add_provider(Beev2Provider)
