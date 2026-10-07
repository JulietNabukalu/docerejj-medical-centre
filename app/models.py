from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql.expression import null

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email=Column(String, nullable=False,unique=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    prescriptions = relationship("Prescription", back_populates="doctor")
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    phone = Column(String, nullable=True)

    age = Column(Integer, nullable=True)

    sex = Column(String, nullable=True)

    prescriptions = relationship(
        "Prescription",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    sales = relationship(
        "Sale",
        back_populates="patient"
    )

class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    #owner_id =Column(Integer,ForeignKey("users.id",ondelete="CASCADE        "))


    sale_items = relationship(
        "SaleItem",
        back_populates="drug"
    )

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    diagnosis = Column(
        String,
        nullable=False
    )

    treatment_plan = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="pending"
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    patient = relationship(
        "Patient",
        back_populates="prescriptions"
    )

    doctor = relationship(
        "User",
        back_populates="prescriptions"
    )
    items = relationship(
        "PrescriptionItem",
        back_populates="prescription",
        cascade="all, delete-orphan"
    )

class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    prescription_id = Column(
        Integer,
        ForeignKey("prescriptions.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    dose_instructions = Column(
        String,
        nullable=True
    )

    prescription = relationship(
        "Prescription",
        back_populates="items"
    )

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    total_amount = Column(
        Float,
        nullable=False,
        default=0
    )

    payment_method = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    patient = relationship(
        "Patient",
        back_populates="sales"
    )

    items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan"
    )
class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)

    sale_id = Column(
        Integer,
        ForeignKey("sales.id"),
        nullable=False
    )

    drug_id = Column(
        Integer,
        ForeignKey("drugs.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Float,
        nullable=False
    )

    total = Column(
        Float,
        nullable=False
    )

    sale = relationship(
        "Sale",
        back_populates="items"
    )

    drug = relationship(
        "Drug",
        back_populates="sale_items"
    )