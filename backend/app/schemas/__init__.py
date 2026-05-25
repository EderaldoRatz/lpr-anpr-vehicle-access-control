"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=120)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class VehicleBase(BaseModel):
    plate: str = Field(..., min_length=3, max_length=20)
    model: str
    color: Optional[str] = None
    brand: str
    vehicle_type: str = "car"
    description: Optional[str] = None


class VehicleCreate(VehicleBase):
    owner_id: str


class VehicleResponse(VehicleBase):
    id: str
    plate_normalized: str
    owner_id: str
    photo_path: Optional[str] = None
    is_authorized: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class OwnerBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None


class OwnerCreate(OwnerBase):
    pass


class OwnerResponse(OwnerBase):
    id: str
    photo_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AccessLogResponse(BaseModel):
    id: str
    plate: str
    vehicle_id: Optional[str] = None
    owner_id: Optional[str] = None
    access_type: str
    is_authorized: bool
    confidence: Optional[str] = None
    image_path: Optional[str] = None
    timestamp: datetime
    gate_opened: bool
    
    class Config:
        from_attributes = True


class CameraConfigResponse(BaseModel):
    id: str
    name: str
    camera_type: str
    source: str
    fps: int
    resolution: str
    is_active: bool
    location: Optional[str] = None
    
    class Config:
        from_attributes = True
