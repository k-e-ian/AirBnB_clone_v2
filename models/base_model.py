#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    if models.storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime(), nullable=False, default=datetime.utcnow())
        updated_at = Column(DateTime(), nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        ''' instanciates a new model '''
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(type(self).name, self.id, self.__dict__)

    def __repr__(self):
        '''return string representation'''
        return self.__str__()

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': self.__class__.__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary.keys():
            del(dictionary["_sa_instance_state"])
        return dictionary

    def delete(self):
        ''' delete current instance from storage <models.storage> '''
        storage.delete(self)
