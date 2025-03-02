# Import necessary modules from SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Define a naming convention for foreign keys to ensure consistency
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)  # Apply the naming convention

# Create a base class for declarative models, using the defined metadata
Base = declarative_base(metadata=metadata)

# Create an SQLite database engine with echo disabled (no SQL output in console)
engine = create_engine('sqlite:///freebies.db', echo=False)

# Create a session factory and a scoped session to manage database transactions
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

# Define an association table for the many-to-many relationship between Dev and Company
dev_company_association = Table(
    'dev_company_association',  # Name of the association table
    Base.metadata,
    Column('dev_id', Integer, ForeignKey('devs.id')),  # Foreign key to Dev
    Column('company_id', Integer, ForeignKey('companies.id'))  # Foreign key to Company
)

# Define the Company model
class Company(Base):
    __tablename__ = 'companies'  # Name of the table in the database

    id = Column(Integer, primary_key=True)  # Unique identifier for each company
    name = Column(String, nullable=False)  # Company name (cannot be null)
    founding_year = Column(Integer, nullable=False)  # Year the company was founded

    # Relationship: A company can have multiple freebies
    freebies = relationship('Freebie', back_populates='company', cascade="all, delete-orphan")

    # Many-to-many relationship with Devs through the association table
    devs = relationship('Dev', secondary=dev_company_association, back_populates='companies')

    def __repr__(self):
        """String representation of the Company object."""
        return f'<Company {self.name} (Founded {self.founding_year})>'

    def give_freebie(self, dev, item_name, value):
        """Creates and assigns a new Freebie to a Dev from this company."""
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)  # Add the new freebie to the session
        session.commit()  # Commit the transaction to save changes
        return freebie

    @classmethod
    def oldest_company(cls):
        """Returns the oldest company based on founding year."""
        return session.query(cls).order_by(cls.founding_year).first()

# Define the Developer (Dev) model
class Dev(Base):
    __tablename__ = 'devs'  # Table name in the database

    id = Column(Integer, primary_key=True)  # Unique identifier for each developer
    name = Column(String, nullable=False)  # Developer name (cannot be null)

    # Relationship: A developer can have multiple freebies
    freebies = relationship('Freebie', back_populates='dev', cascade="all, delete-orphan")

    # Many-to-many relationship with Companies through the association table
    companies = relationship('Company', secondary=dev_company_association, back_populates='devs')

    def __repr__(self):
        """String representation of the Dev object."""
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        """Checks if the developer has received a freebie with the given name."""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        """Transfers a freebie to another developer if the current developer owns it."""
        if freebie in self.freebies:  # Ensure the developer owns the freebie
            freebie.dev = dev  # Change ownership to the new developer
            session.commit()  # Commit the transaction to save changes

# Define the Freebie model
class Freebie(Base):
    __tablename__ = 'freebies'  # Table name in the database

    id = Column(Integer, primary_key=True)  # Unique identifier for each freebie
    item_name = Column(String, nullable=False)  # Name of the freebie (cannot be null)
    value = Column(Integer)  # Value of the freebie

    # Foreign keys: Each freebie belongs to one Dev and one Company
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    # Relationships: A freebie belongs to one Dev and one Company
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    def __repr__(self):
        """String representation of the Freebie object."""
        return f'<Freebie {self.item_name} from {self.company.name if self.company else "Unknown"}>'

    def print_details(self):
        """Returns a formatted string describing the freebie's ownership."""
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'

# Create the database tables if they do not already exist
Base.metadata.create_all(engine)












# from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
#from sqlalchemy.orm import relationship, backref
#from sqlalchemy.ext.declarative import declarative_base

#convention = {
   # "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#}
#metadata = MetaData(naming_convention=convention)

#Base = declarative_base(metadata=metadata)

#class Company(Base):
   # __tablename__ = 'companies'

    #id = Column(Integer(), primary_key=True)
   # name = Column(String())
   # founding_year = Column(Integer())

   # def __repr__(self):
        #return f'<Company {self.name}>'

#class Dev(Base):
   # __tablename__ = 'devs'

    #id = Column(Integer(), primary_key=True)
    #name= Column(String())

    #def __repr__(self):
       # return f'<Dev {self.name}>'
