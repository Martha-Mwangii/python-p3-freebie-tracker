#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base

# Database connection
engine = create_engine('sqlite:///freebies.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Clear existing data to prevent duplicates
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()
session.commit()

# Sample data
companies_data = [
    {'name': 'Company X', 'founding_year': 2005},
    {'name': 'Company Y', 'founding_year': 2012},
    {'name': 'Company Z', 'founding_year': 1998}
]

devs_data = [
    {'name': 'Developer 1'},
    {'name': 'Developer 2'},
    {'name': 'Developer 3'}
]

freebies_data = [
    {'item_name': 'T-shirt', 'value': 20, 'dev_id': 1, 'company_id': 1},
    {'item_name': 'Mug', 'value': 10, 'dev_id': 2, 'company_id': 2},
    {'item_name': 'Sticker', 'value': 5, 'dev_id': 3, 'company_id': 3},
]

# Insert companies
companies = []
for company_data in companies_data:
    company = Company(**company_data)
    session.add(company)
    companies.append(company)

# Insert developers
devs = []
for dev_data in devs_data:
    dev = Dev(**dev_data)
    session.add(dev)
    devs.append(dev)

# Commit companies and devs first so they have IDs
session.commit()

# Insert freebies
for freebie_data in freebies_data:
    freebie = Freebie(**freebie_data)
    session.add(freebie)

# Commit freebies
session.commit()

print("Database seeded successfully!")

# Close session
session.close()

