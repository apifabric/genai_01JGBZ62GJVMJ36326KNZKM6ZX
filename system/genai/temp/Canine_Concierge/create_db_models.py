# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class DogOwner(Base):
    """description: Represents a dog owner who registers for dog walking services."""
    __tablename__ = 'dog_owner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(100))

class Dog(Base):
    """description: Represents a dog under the care of a dog owner."""
    __tablename__ = 'dog'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    breed = Column(String(50))
    owner_id = Column(Integer, ForeignKey('dog_owner.id'))

class Walker(Base):
    """description: Represents a person who provides dog walking services."""
    __tablename__ = 'walker'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    phone = Column(String(15))

class Appointment(Base):
    """description: Represents an appointment for dog walking services."""
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dog_id = Column(Integer, ForeignKey('dog.id'))
    walker_id = Column(Integer, ForeignKey('walker.id'))
    date = Column(DateTime)

class Service(Base):
    """description: Represents a type of dog walking service offered."""
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_type = Column(String(50))
    description = Column(String(255))
    price = Column(Float)

class AppointmentService(Base):
    """description: Associates services with specific appointments."""
    __tablename__ = 'appointment_service'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'))
    service_id = Column(Integer, ForeignKey('service.id'))

class Payment(Base):
    """description: Represents a payment made for dog walking services."""
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float)
    date = Column(DateTime)
    method = Column(String(50))
    appointment_id = Column(Integer, ForeignKey('appointment.id'))

class Invoice(Base):
    """description: Represents an invoice for an appointment's services and payments."""
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey('payment.id'))
    amount_due = Column(Float)
    date_issued = Column(DateTime)

class WalkerAvailability(Base):
    """description: Stores the availability of walkers on specific dates."""
    __tablename__ = 'walker_availability'
    id = Column(Integer, primary_key=True, autoincrement=True)
    walker_id = Column(Integer, ForeignKey('walker.id'))
    date = Column(Date)
    available = Column(Boolean)

class AppointmentReview(Base):
    """description: Represents a review left for an appointment."""
    __tablename__ = 'appointment_review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'))
    rating = Column(Integer)
    comment = Column(String(255))

class Discount(Base):
    """description: Represents discount codes available for use."""
    __tablename__ = 'discount'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20))
    percentage = Column(Float)
    description = Column(String(255))

class AppointmentDiscount(Base):
    """description: Associates discounts applied to appointments."""
    __tablename__ = 'appointment_discount'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'))
    discount_id = Column(Integer, ForeignKey('discount.id'))


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    dog_owner_1 = DogOwner(name="Alice Walker", email="alice@example.com")
    dog_owner_2 = DogOwner(name="Bob Smith", email="bob@example.com")
    dog_owner_3 = DogOwner(name="Charlie Brown", email="charlie@example.com")
    dog_owner_4 = DogOwner(name="Diana Prince", email="diana@example.com")
    dog_1 = Dog(name="Rover", breed="Labrador", owner_id=1)
    dog_2 = Dog(name="Max", breed="Golden Retriever", owner_id=2)
    dog_3 = Dog(name="Buddy", breed="Beagle", owner_id=3)
    dog_4 = Dog(name="Luna", breed="Poodle", owner_id=4)
    walker_1 = Walker(name="Jake Park", phone="123-456-7890")
    walker_2 = Walker(name="Ella Rose", phone="234-567-8901")
    appointment_1 = Appointment(dog_id=1, walker_id=1, date=datetime(2023, 10, 20, 10, 0))
    appointment_2 = Appointment(dog_id=2, walker_id=2, date=datetime(2023, 10, 21, 12, 0))
    service_1 = Service(service_type="Regular Walk", description="30-minute walk", price=15.00)
    service_2 = Service(service_type="Extended Walk", description="60-minute walk", price=25.00)
    appointment_service_1 = AppointmentService(appointment_id=1, service_id=1)
    appointment_service_2 = AppointmentService(appointment_id=2, service_id=2)
    payment_1 = Payment(amount=15.00, date=datetime(2023, 10, 20, 11, 0), method="Credit Card", appointment_id=1)
    payment_2 = Payment(amount=25.00, date=datetime(2023, 10, 21, 13, 0), method="Cash", appointment_id=2)
    invoice_1 = Invoice(payment_id=1, amount_due=15.00, date_issued=datetime(2023, 10, 22))
    invoice_2 = Invoice(payment_id=2, amount_due=25.00, date_issued=datetime(2023, 10, 23))
    walker_availability_1 = WalkerAvailability(walker_id=1, date=date(2023, 10, 20), available=True)
    walker_availability_2 = WalkerAvailability(walker_id=2, date=date(2023, 10, 21), available=True)
    appointment_review_1 = AppointmentReview(appointment_id=1, rating=5, comment="Great service!")
    appointment_review_2 = AppointmentReview(appointment_id=2, rating=4, comment="Good walk, but a bit late.")
    discount_1 = Discount(code="WELCOME10", percentage=10.0, description="10% off your first appointment")
    discount_2 = Discount(code="SUMMERFUN", percentage=15.0, description="15% off during summer")
    appointment_discount_1 = AppointmentDiscount(appointment_id=1, discount_id=1)
    appointment_discount_2 = AppointmentDiscount(appointment_id=2, discount_id=2)
    
    
    
    session.add_all([dog_owner_1, dog_owner_2, dog_owner_3, dog_owner_4, dog_1, dog_2, dog_3, dog_4, walker_1, walker_2, appointment_1, appointment_2, service_1, service_2, appointment_service_1, appointment_service_2, payment_1, payment_2, invoice_1, invoice_2, walker_availability_1, walker_availability_2, appointment_review_1, appointment_review_2, discount_1, discount_2, appointment_discount_1, appointment_discount_2])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
