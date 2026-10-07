from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional



class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    role: str

    email:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel) :
      access_token: str
      token_type:str

class TokenData(BaseModel):
    id:int


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True



class PatientCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None


class PatientResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None

    class Config:
        from_attributes = True



class DrugCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int = 0
    #owner_id:int

class DrugUpdate(BaseModel):
    name: str
    price: float
    stock_quantity: int

class DrugResponse(BaseModel):
    id: int
    name: str
    price: float
    stock_quantity: int
    #owner_id:int




    class Config:
        from_attributes = True



class PrescriptionItemCreate(BaseModel):
    drug_id: int
    quantity: int
    dose_instructions: Optional[str] = None


class PrescriptionItemResponse(BaseModel):
    id: int
    prescription_id: int
    drug_id: int
    quantity: int
    dose_instructions: Optional[str] = None

    class Config:
        from_attributes = True



class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    diagnosis: str
    treatment_plan: Optional[str] = None
    items: list[PrescriptionItemCreate] = []


class PrescriptionResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: Optional[int] = None
    diagnosis: str
    treatment_plan: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True



class SaleItemCreate(BaseModel):
    drug_id: int
    quantity: int
    unit_price: float
    total: float


class SaleItemResponse(BaseModel):
    id: int
    sale_id: int
    drug_id: int
    quantity: int
    unit_price: float
    total: float

    class Config:
        from_attributes = True




class SaleCreate(BaseModel):
    patient_id: Optional[int] = None
    total_amount: float = 0
    payment_method: Optional[str] = None
    items: list[SaleItemCreate] = []


class SaleResponse(BaseModel):
    id: int
    patient_id: Optional[int] = None
    total_amount: float
    payment_method: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class VoiceDrugCommand(BaseModel):
    text: str

class SaleItemCreate(BaseModel):
    drug_id: int
    quantity: int


class SaleCreate(BaseModel):
    patient_id: int | None = None
    payment_method: str | None = None
    items: list[SaleItemCreate]