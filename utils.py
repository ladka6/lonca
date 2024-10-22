import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
from product import Product


def convert_key(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-ZÇĞİÖŞÜ])", "_", s).lower()


def parse_description(description: ET.Element, document: dict) -> None:
    description_html = description.text or ""

    soup = BeautifulSoup(description_html, "html.parser")

    for li in soup.find_all("li"):
        strong_tag = li.find("strong")
        if strong_tag:
            key = convert_key(
                strong_tag.get_text(strip=True).replace(":", "").replace(" ", "")
            )

            key = re.sub(r"\d+", "", key).strip()
            value = li.get_text(strip=True).replace(strong_tag.get_text(strip=True), "")
            document[key] = value
            if key == "model_ölçüleri":
                break


def has_differences(existing_product: Product, new_data: Dict[str, Any]) -> bool:
    for key, value in new_data.items():
        existing_value = getattr(existing_product, key, None)
        if existing_value != value:
            return True
    return False


def preprocess_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Preprocesses the raw data dictionary and returns a processed dictionary suitable for the Product model."""
    discounted_price_str: Optional[str] = data.get("discounted_price")
    price_str: Optional[str] = data.get("price")
    quantity_str: Optional[str] = data.get("quantity")

    processed_data: Dict[str, Any] = {
        "stock_code": data.get("stock_code"),
        "color": data.get("color"),
        "discounted_price": (
            float(discounted_price_str.replace(",", "."))
            if discounted_price_str
            else None
        ),
        "images": data.get("images"),
        "is_discounted": bool(
            discounted_price_str and float(discounted_price_str.replace(",", ".")) > 0
        ),
        "name": data.get("ürün_bilgisi"),
        "price": float(price_str.replace(",", ".")) if price_str else None,
        "product_type": data.get("product_type"),
        "quantity": int(quantity_str) if quantity_str else 0,
        "sample_size": data.get("series"),
        "series": data.get("series"),
        "fabric": data.get("kumaş_bilgisi"),
        "model_measurements": data.get("model_ölçüleri"),
        "product_measurements": data.get("ürün_ölçüleri"),
    }
    return processed_data
