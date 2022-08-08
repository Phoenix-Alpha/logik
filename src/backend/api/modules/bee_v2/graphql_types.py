import strawberry

from .models import Article as ArticleModel
from .models import Barcode as BarcodeModel


@strawberry.experimental.pydantic.type(all_fields=True, model=BarcodeModel)
class Barcode:
    pass


@strawberry.experimental.pydantic.type(all_fields=True, model=ArticleModel)
class Article:
    pass
