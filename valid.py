"""
Task: Build a Pydantic model for a “User Registration System”
Interns should create Pydantic models that validate:
1. User Information
first_name: string
last_name: string
email: string
phone: optional string
age: integer (must be 18+, validator)
registered_at: date (string in JSON → parsed into date)
fullName (alias for full_name field)
2. Address (Nested Model)
Fields:
street: str
city: str
pincode: int
This must be included under:
"address": { ... }
3. Skills (List Example)
skills: list of strings
Must contain at least 1 skill (validator required)
4. Combine all into a Main Model
{"fullName": "Sachin Kharat","email": "sachin@example.com","age": "22","phone": null,"registered_at": "2024-12-01","skills": ["python", "selenium", "fastapi"],"address": {"street": "Palm Avenue","city": "Mumbai","pincode": "400001"} } 
 Things They Must Implement (Checklist)
 1. A main User model
 2. Use alias="fullName"
 3. Optional field (phone)
 4. Type conversions (age & pincode strings → int)
 5. Validator for:
age >= 18
skills list not empty
 6. Nested Address model
 7. Parse the raw JSON using .model_validate()
 8. Print output using .model_dump(by_alias=True)
 """



from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class Address(BaseModel):
    street: str
    city: str
    pincode: int   

    @field_validator("pincode")
    def convert_pincode(cls, v):
        return int(v)


class User(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone: Optional[int] = None
    age: int
    registered_at: date
    full_name: str = Field(alias="fullName")
    skills: List[str]
    address: Address

    @field_validator("age")
    def validate_age_type(cls, v):
        return int(v)

    @field_validator("age")
    def validate_age_minimum(cls, v):
        if v < 18:
            raise ValueError("Age must be 18 or above")
        return v

    @field_validator("skills")
    def validate_skills(cls, v):
        if not v:
            raise ValueError("At least one skill required")
        return v


# Raw json
raw_json = {
    "fullName": "Sachin Kharat",
    "email": "sachin@example.com",
    "age": "23",
    "phone": 9555025078,
    "registered_at": "2024-12-01",
    "skills": ["python", "selenium", "fastapi"],
    "address": {
        "street": "Palm Avenue",
        "city": "Mumbai",
        "pincode": "400001"
    }
}


user = User.model_validate(raw_json)


print(user.model_dump(by_alias=True))
