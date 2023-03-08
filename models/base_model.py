#!/usr/bin/python3
""" Module that contain the basemodel for the project"""
from uuid import uuid4
from models import storage
from datetime import datetime


class BaseModel:
    """A base model class to create an instance"""

    def __init__(self, *args, **kwargs):
        """Initialize the Basemdodel"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        value = datetime.fromisoformat(value)
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
            storage.save()

    def __str__(self):
        """ Return string representation of an object"""
        return "[{}] ({}) {}".format(type(self).__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Save changes made to an object"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert object to dictionary"""
        new_dict = {}
        new_dict["__class__"] = type(self).__name__

        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                new_dict[key] = value.isoformat()
            else:
                new_dict[key] = value

        return new_dict
