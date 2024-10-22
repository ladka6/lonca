# Product XML Processor

This project processes an XML file of products, extracts relevant data, and stores or updates the product information in a MongoDB database. The script uses MongoEngine for database interaction and supports updating existing products or inserting new ones.

## Features

- **XML Parsing**: Extracts product information from an XML file.
- **MongoDB Integration**: Connects to MongoDB to fetch, update, or insert product data.
- **Data Preprocessing**: Handles conversion and preprocessing of XML data to match the database schema.
- **Logging**: Logs all important actions and errors for easier debugging.

## Requirements

- Python 3.x
- MongoDB
- Python packages:
  - `mongoengine`
  - `beautifulsoup4`
  - `lxml`
  - `xml.etree.ElementTree`
  - `re`
  - `logging`

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/product-processor.git
   cd product-processor
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up a MongoDB database. You can use Docker to quickly run a MongoDB instance:
   ```bash
   docker-compose up -d
   ```
4. Prepare your XML file with the products. The sample XML file is named `lonca-sample.xml` in this example.

# Running the Processor

To run the product processor, execute the following command

    python main.py

This will:

- Parse the XML file and extract product data.
- Connect to the MongoDB database.
- Fetch existing products by ProductId (stock code) from the database.
- Compare existing products with new data and update them if there are changes.
- Insert new products if they don't exist in the database.

# Project Structure

`main.py`: Main file that runs the program.

`processor.py`: Processor class that handles XML parsing, MongoDB connection, and product data processing.

`product.py`: Defines the MongoEngine Product model.

`utils.py`: Contains utility functions for preprocessing data and checking for differences between existing and new product data.

`lonca-sample.xml`: Sample XML file for testing (to be provided by the user).

# Example XML Structure

```
<Products>
  <Product ProductId="12345">
    <ProductDetails>
      <Detail Name="Name" Value="Product Name" />
      <Detail Name="Color" Value="Red" />
    </ProductDetails>
    <Images>
      <Image Path="image1.jpg" />
    </Images>
    <Description>
      <![CDATA[
        <ul>
          <li><strong>Model:</strong> Model information here</li>
          <li><strong>Measurements:</strong> Measurements here</li>
        </ul>
      ]]>
    </Description>
  </Product>
</Products>
```

# MongoDB Product Schema

The `Product` model is defined in `product.py`. It contains fields like:

`stock_code`: Unique product identifier.

`name`: Name of the product.

`color`: List of product colors.

`price`: Price of the product.

`discounted_price`: Discounted price, if available.

`quantity`: Number of available items.

`images`: List of image paths.

`product_type`, fabric, series: Other product attributes.

`createdAt`: Timestamp of the first insert.

`updatedAt`: Timestamp of the last update.

# Logs

Logs will be generated during the process to track successful operations and errors. They include:

- Successful database connections.
- Parsing information about the XML file.
- Product updates and insertions.
- Error messages for database connection or XML parsing failures.
