#!/usr/bin/python3
"""
This is the console base for the unit
"""
import cmd
import json
import shlex
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """A class that implements the cmd module"""
    prompt = '(hbnb) '

    models = {"BaseModel": BaseModel, "User": User, "Place": Place,
              "City": City, "Review": Review, "Amenity": Amenity}
    commands = ['create', 'destroy', 'all', 'update', 'show', 'count']

    def precmd(self, line):
        """Parse command input"""
        H = HBNBCommand
        if '.' in line and '(' in line and ')' in line:
            inputs = line.split('.')
            model = inputs[0]
            command = inputs[1].split('(')
            arg = command[1].split(')')[0]
            command = command[0]
            if model in H.models.keys() and command in H.commands:
                line = command + ' ' + model + ' ' + arg
        return (line)

    def do_EOF(self, line):
        """Execute the program"""
        return True

    def do_quit(self, line):
        """quit the command promt"""
        return True

    def emptyline(self):
        """overide default emptyline"""
        pass

    def do_create(self, line):
        """creates a new instances of the BaseModel"""
        if not line:
            print("** class name missing **")
            return
        commands = shlex.split(line)
        if commands[0] not in HBNBCommand.models.keys():
            print("** class doenst exist **")
            return
        new_instance = HBNBCommand.models[commands[0]]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """show instance of a model"""
        if not line:
            print("** class name missing **")
            return
        commands = shlex.split(line)
        if commands[0] not in HBNBCommand.models.keys():
            print("** class doenst exist **")
            return
        if len(commands) <= 1:
            print("** instance id missing **")
            return
        objects = storage.all()
        key = commands[0] + '.' + commands[1]
        if key in objects.keys():
            print(str(objects[key]))
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """Destroy an instance of a model"""

        if not line:
            print("** class name missing **")
            return
        commands = shlex.split(line)
        if commands[0] not in HBNBCommand.models.keys():
            print("** class doenst exist **")
            return
        if len(commands) <= 1:
            print("** instance id missing **")
            return
        objects = storage.all()
        key = commands[0] + '.' + commands[1]
        if key in objects.keys():
            objects.pop(key)
            storage.save()
        else:
            print("** instance not found **")

    def do_all(self, line):
        """print all instances of a model"""
        if not line:
            print("** class name missing **")
            return
        commands = shlex.split(line)
        if commands[0] not in HBNBCommand.models.keys():
            print("** class doenst exist **")
            return
        objects = storage.all()
        my_json = []
        for key, value in objects.items():
            key = key.split('.')[0]
            if key == commands[0]:
                my_json.append(str(value))
        print(my_json)

    def do_update(self, line):
        """ update an instance base on fthe class name and id"""
        if not line:
            print("** class name missing **")
            return
        commands = shlex.split(line)
        if commands[0] not in HBNBCommand.models.keys():
            print("** class doenst exist **")
            return
        if len(commands) == 1:
            print("** instance id missing **")
            return
        if len(commands) == 2:
            print("** attribute name missing **")
            return
        if len(commands) == 3:
            print("** value missing **")
            return
        objects = storage.all()
        key = commands[0] + '.' + commands[1].rstrip(',')
        if key not in objects.keys():
            print("** no instance found **")
        for keys, value in objects.items():
            if key == keys:
                if commands[2].startswith("{"):
                    print("starting")
                    self.do_update2(line)
                    return
                if hasattr(value, commands[2]):
                    data_type = type(getattr(value, commands[2]))
                    setattr(value, commands[2].rstrip(','),
                            data_type(commands[3].rstrip(',')))
                else:
                    setattr(value, commands[2].rstrip(','),
                            commands[3].rstrip(','))
        storage.save()

    def do_update2(self, line):
        """ update an instance base on fthe class name and id"""
        print("second update method")
        if not line:
            print("** class name missing **")
            return
        temp_dict = "{" + line.split("{")[1]
        temp_dict = temp_dict.replace("\'", "\"")
        commands = shlex.split(line)
        if commands[0] not in HBNBCommand.models.keys():
            print("** class doenst exist **")
            return
        if len(commands) == 1:
            print("** instance id missing **")
            return
        if len(commands) == 2:
            print("** attribute name missing **")
            return
        if len(commands) == 3:
            print("** value missing **")
            return
        objects = storage.all()
        key = commands[0] + '.' + commands[1].rstrip(',')
        if key not in objects.keys():
            print("** no instance found **")
        for keys, value in objects.items():
            if key == keys:
                print(f"{temp_dict} {type(temp_dict)}")
                temp_dict = json.loads(temp_dict)
                print(f"{type(temp_dict)} {type(dict())} {temp_dict}")
                for key1, value1 in temp_dict.items():
                    if hasattr(value, key1):
                        data_type = type(getattr(value, key1))
                        setattr(value, key1, data_type(value1))
                    else:
                        setattr(value, key1, value1)

    def do_count(self, line):
        """count the number of instances of a class"""

        if not line:
            print("** class name missing **")
            return
        commands = shlex.split(line)
        if commands[0] not in HBNBCommand.models.keys():
            print("** class doenst exist **")
            return
        count = 0
        data = storage.all()
        for key in data.keys():
            if commands[0] == key.split('.')[0]:
                count += 1

        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
