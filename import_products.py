import csv
from db import Model, Session, engine
from models import Product


def main():
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open('products.csv') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['year'] = int(row['year'])
                    product = Product(**row)
                    session.add(product)

if __name__ == '__main__':
    main()