import xml.etree.ElementTree as ET
from mongoengine import connect
from product import Product
from datetime import datetime, timezone
from utils import convert_key, parse_description, has_differences, preprocess_data
import logging

logging.basicConfig(level=logging.INFO)


class Processor:
    def __init__(self, xml_file: str, db_host: str):
        self.xml_file = xml_file
        self.db_host = db_host
        self.root = self.parse_xml()
        self.connect_db()

    def connect_db(self) -> None:
        """Establish a connection to the MongoDB database."""
        try:
            connect(host=self.db_host)
            logging.info("Connected to the database.")
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def parse_xml(self) -> ET.Element:
        """Parse the XML file and return the root element."""
        try:
            tree = ET.parse(self.xml_file)
            logging.info(f"Parsed XML file: {self.xml_file}")
            return tree.getroot()
        except ET.ParseError as e:
            logging.error(f"Failed to parse XML file: {e}")
            raise

    def fetch_existing_products(self, stock_codes: list) -> dict:
        """Fetch existing products from the database."""
        try:
            products = Product.objects(stock_code__in=stock_codes)
            logging.info("Fetched existing products from database.")
            return {p.stock_code: p for p in products}
        except Exception as e:
            logging.error(f"Error fetching existing products: {e}")
            return {}

    def build_document(self, product: ET.Element) -> dict:
        """Build a document dictionary from an XML product element."""
        document: dict = {}
        try:
            stock_code = product.attrib["ProductId"]
            document["stock_code"] = stock_code
        except KeyError:
            logging.error(f"ProductId missing in product: {product}")
            return None

        for details in product:
            if details.tag == "Images":
                document["images"] = [image.attrib["Path"] for image in details]
            elif details.tag == "ProductDetails":
                document["color"] = []
                for detail in details:
                    detail_name = convert_key(detail.attrib["Name"])
                    detail_value = detail.attrib["Value"]
                    if detail_name == "color":
                        document["color"].append(detail_value)
                    else:
                        document[detail_name] = detail_value
            elif details.tag == "Description":
                parse_description(details, document)

        document = preprocess_data(document)
        return document

    def update_product(self, existing_product: Product, document: dict) -> None:
        """Update an existing product in the database."""
        update_dict = {f"set__{key}": value for key, value in document.items()}
        update_dict["set__updatedAt"] = datetime.now(timezone.utc)
        try:
            existing_product.update(**update_dict)
        except Exception as e:
            logging.error(f"Error updating product {existing_product.stock_code}: {e}")

    def insert_product(self, document: dict) -> None:
        """Insert a new product into the database."""
        try:
            product_instance = Product(**document)
            product_instance.save()
        except Exception as e:
            logging.error(f"Error inserting product {document['stock_code']}: {e}")

    def update_or_insert_product(self, document: dict, existing_products: dict) -> None:
        """Update an existing product or insert a new one."""
        if document is None:
            logging.error("Document is None, skipping product.")
            return
        stock_code = document["stock_code"]
        existing_product = existing_products.get(stock_code)
        if existing_product:
            if has_differences(existing_product, document):
                self.update_product(existing_product, document)
                logging.info(f"Product {stock_code} updated.")
            else:
                logging.info(
                    f"No changes detected for product {stock_code}. Update skipped."
                )
        else:
            self.insert_product(document)
            logging.info(f"Product {stock_code} inserted.")

    def process_products(self) -> None:
        """Process all products in the XML file."""
        stock_codes = [product.attrib["ProductId"] for product in self.root]
        existing_products = self.fetch_existing_products(stock_codes)

        for product in self.root:
            document = self.build_document(product)
            self.update_or_insert_product(document, existing_products)
