from pydantic import BaseModel,EmailStr, Field
from typing import Optional
class Student(BaseModel):
    name : str = 'nitish'
    age : Optional[int] = None
    email : EmailStr
    cg : float = Field(gt=0,lt=10)

new_stud = {'age':32,'email':'abc@gmail.com','cg':1}
student = Student(**new_stud)
#convert into dictionary
st_dict= student.model_dump()
#or convert into json
st_json = student.model_dump_json() 
print(student)