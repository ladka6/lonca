from mongoengine import (
    Document,
    StringField,
    ListField,
    FloatField,
    BooleanField,
    IntField,
    DateTimeField,
)
from datetime import datetime, timezone


class Product(Document):
    stock_code = StringField(required=True)
    color = ListField(StringField(), required=True)
    discounted_price = FloatField()
    images = ListField(StringField())
    is_discounted = BooleanField(default=False)
    name = StringField(required=True)
    price = FloatField(required=True)
    price_unit = StringField(default="USD")
    product_type = StringField(required=True)
    quantity = IntField(required=True)
    sample_size = StringField()
    series = StringField()
    status = StringField(default="Active")
    fabric = StringField()
    model_measurements = StringField()
    product_measurements = StringField()
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updatedAt = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {"collection": "product"}
