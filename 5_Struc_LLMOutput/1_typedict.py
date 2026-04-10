from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int

new_p : Person={'name':'raj','age':32}

print(new_p)