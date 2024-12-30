# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 30, 2024 14:24:11
# Database: sqlite:////tmp/tmp.jTwuK6JVtU-01JGBZ62GJVMJ36326KNZKM6ZX/Canine_Concierge/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

Base = SAFRSBaseX



class Discount(Base):  # type: ignore
    """
    description: Represents discount codes available for use.
    """
    __tablename__ = 'discount'
    _s_collection_name = 'Discount'  # type: ignore

    id = Column(Integer, primary_key=True)
    code = Column(String(20))
    percentage = Column(Float)
    description = Column(String(255))

    # parent relationships (access parent)

    # child relationships (access children)
    AppointmentDiscountList : Mapped[List["AppointmentDiscount"]] = relationship(back_populates="discount")



class DogOwner(Base):  # type: ignore
    """
    description: Represents a dog owner who registers for dog walking services.
    """
    __tablename__ = 'dog_owner'
    _s_collection_name = 'DogOwner'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

    # parent relationships (access parent)

    # child relationships (access children)
    DogList : Mapped[List["Dog"]] = relationship(back_populates="owner")



class Service(Base):  # type: ignore
    """
    description: Represents a type of dog walking service offered.
    """
    __tablename__ = 'service'
    _s_collection_name = 'Service'  # type: ignore

    id = Column(Integer, primary_key=True)
    service_type = Column(String(50))
    description = Column(String(255))
    price = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    AppointmentServiceList : Mapped[List["AppointmentService"]] = relationship(back_populates="service")



class Walker(Base):  # type: ignore
    """
    description: Represents a person who provides dog walking services.
    """
    __tablename__ = 'walker'
    _s_collection_name = 'Walker'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(String(15))

    # parent relationships (access parent)

    # child relationships (access children)
    WalkerAvailabilityList : Mapped[List["WalkerAvailability"]] = relationship(back_populates="walker")
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="walker")



class Dog(Base):  # type: ignore
    """
    description: Represents a dog under the care of a dog owner.
    """
    __tablename__ = 'dog'
    _s_collection_name = 'Dog'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    breed = Column(String(50))
    owner_id = Column(ForeignKey('dog_owner.id'))

    # parent relationships (access parent)
    owner : Mapped["DogOwner"] = relationship(back_populates=("DogList"))

    # child relationships (access children)
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="dog")



class WalkerAvailability(Base):  # type: ignore
    """
    description: Stores the availability of walkers on specific dates.
    """
    __tablename__ = 'walker_availability'
    _s_collection_name = 'WalkerAvailability'  # type: ignore

    id = Column(Integer, primary_key=True)
    walker_id = Column(ForeignKey('walker.id'))
    date = Column(Date)
    available = Column(Boolean)

    # parent relationships (access parent)
    walker : Mapped["Walker"] = relationship(back_populates=("WalkerAvailabilityList"))

    # child relationships (access children)



class Appointment(Base):  # type: ignore
    """
    description: Represents an appointment for dog walking services.
    """
    __tablename__ = 'appointment'
    _s_collection_name = 'Appointment'  # type: ignore

    id = Column(Integer, primary_key=True)
    dog_id = Column(ForeignKey('dog.id'))
    walker_id = Column(ForeignKey('walker.id'))
    date = Column(DateTime)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("AppointmentList"))
    walker : Mapped["Walker"] = relationship(back_populates=("AppointmentList"))

    # child relationships (access children)
    AppointmentDiscountList : Mapped[List["AppointmentDiscount"]] = relationship(back_populates="appointment")
    AppointmentReviewList : Mapped[List["AppointmentReview"]] = relationship(back_populates="appointment")
    AppointmentServiceList : Mapped[List["AppointmentService"]] = relationship(back_populates="appointment")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="appointment")



class AppointmentDiscount(Base):  # type: ignore
    """
    description: Associates discounts applied to appointments.
    """
    __tablename__ = 'appointment_discount'
    _s_collection_name = 'AppointmentDiscount'  # type: ignore

    id = Column(Integer, primary_key=True)
    appointment_id = Column(ForeignKey('appointment.id'))
    discount_id = Column(ForeignKey('discount.id'))

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("AppointmentDiscountList"))
    discount : Mapped["Discount"] = relationship(back_populates=("AppointmentDiscountList"))

    # child relationships (access children)



class AppointmentReview(Base):  # type: ignore
    """
    description: Represents a review left for an appointment.
    """
    __tablename__ = 'appointment_review'
    _s_collection_name = 'AppointmentReview'  # type: ignore

    id = Column(Integer, primary_key=True)
    appointment_id = Column(ForeignKey('appointment.id'))
    rating = Column(Integer)
    comment = Column(String(255))

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("AppointmentReviewList"))

    # child relationships (access children)



class AppointmentService(Base):  # type: ignore
    """
    description: Associates services with specific appointments.
    """
    __tablename__ = 'appointment_service'
    _s_collection_name = 'AppointmentService'  # type: ignore

    id = Column(Integer, primary_key=True)
    appointment_id = Column(ForeignKey('appointment.id'))
    service_id = Column(ForeignKey('service.id'))

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("AppointmentServiceList"))
    service : Mapped["Service"] = relationship(back_populates=("AppointmentServiceList"))

    # child relationships (access children)



class Payment(Base):  # type: ignore
    """
    description: Represents a payment made for dog walking services.
    """
    __tablename__ = 'payment'
    _s_collection_name = 'Payment'  # type: ignore

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    date = Column(DateTime)
    method = Column(String(50))
    appointment_id = Column(ForeignKey('appointment.id'))

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)
    InvoiceList : Mapped[List["Invoice"]] = relationship(back_populates="payment")



class Invoice(Base):  # type: ignore
    """
    description: Represents an invoice for an appointment's services and payments.
    """
    __tablename__ = 'invoice'
    _s_collection_name = 'Invoice'  # type: ignore

    id = Column(Integer, primary_key=True)
    payment_id = Column(ForeignKey('payment.id'))
    amount_due = Column(Float)
    date_issued = Column(DateTime)

    # parent relationships (access parent)
    payment : Mapped["Payment"] = relationship(back_populates=("InvoiceList"))

    # child relationships (access children)
