from processor import Processor

MONGO_URI = "mongodb://root:12345678@localhost:27017/products?authSource=admin"

if __name__ == "__main__":
    processor = Processor(
        xml_file="lonca-sample.xml",
        db_host=MONGO_URI,
    )
    processor.process_products()
