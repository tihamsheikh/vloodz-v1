import inflect 
from typing import Any 
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative 

# inflect enginge initalization 
inflect_engine = inflect.engine() 

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True) 
    __name__: str 

    # Generate table name automatically
    @declared_attr 
    def __tablename__(cls):
        # convert class name to lowercase and pluralize it
        singular_name = cls.__name__.lower()
        plural_name = inflect_engine.plural(singular_name)
        return plural_name
    