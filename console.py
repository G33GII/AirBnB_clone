#!/usr/bin/python3
""" This is a simple console application"""

import cmd
import re
import models
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """This class inherits from the cmd.Cmd class
    and defines the cmmd"""
    prompt = "(hbnb) "
    cls_name = [
        "BaseModel", "User", "State", "City", "Amenity", "Place", "Review"
    ]
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'City': City,
        'Amenity': Amenity,
        'Review': Review,
        'State': State,
    }

    def preloop(self):
        """Called once before the command loop starts"""
        pass

    def default(self, arg):
        """Called for unrecognized commands"""
        ln = arg.strip()
        match = re.match(r'^(\w+)\.all\(\)$', ln)

        if match:
            print("Matched")
            _x = ln.split('.')
            _r = [x for x in _x]
            z = []
            i = 0

            if _r[0] not in HBNBCommand.cls_name:
                print("** class doesn't exist **")
                return
            for k, v in models.storage.all().items():
                if _r[0] in k:
                    z.append(str(v))
            for s in z:
                if i == 0:
                    print("[", end="")
                i += 1
                for c in s:
                    print(c, end="")
                print(", " if i < len(z) else "]")
            return True

        else:
            print(f"*** Unknown syntax: {ln}")
            return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Handles EOF (Ctrl+D) to exit the program"""
        print()
        return True

    def emptyline(self):
        """Empty line should do nothing"""
        pass

    def do_create(self, args):
        """ Create an object of any class
        - Command syntax: "create" <Class name> <param 1> <param 2> <param 3>...
        """
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Extracting parameters from args
        params = {}
        for arg in args[1:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                # Handling string value
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                # Handling float value
                elif '.' in value and all(part.isdigit() for part in value.split('.')):
                    value = float(value)
                # Handling integer value
                elif value.isdigit():
                    value = int(value)
                # Skipping unrecognized values
                else:
                    continue
                params[key] = value

        # Creating instance with parameters
        new_instance = HBNBCommand.classes[class_name](**params)
        storage.save()
        print(new_instance.id)
        storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id"""
        _x = arg.split()
        _r = [x.strip() for x in _x]

        if len(_r) < 1:
            print("** class name missing **")
        elif _r[0] not in HBNBCommand.cls_name:
            print("** class doesn't exist **")
        elif len(_r) < 2:
            print("** instance id missing **")
        elif f"{_r[0]}.{_r[1]}" not in models.storage.all().keys():
            print("** no instance found **")
        else:
            obj = models.storage.all()[f"{_r[0]}.{_r[1]}"]
            print(obj)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        _x = arg.split()
        _r = [x.strip() for x in _x]
        if len(_r) < 1:
            print("** class name missing **")
        elif _r[0] not in HBNBCommand.cls_name:
            print("** class doesn't exist **")
        elif len(_r) < 2:
            print("** instance id missing **")
        elif f"{_r[0]}.{_r[1]}" not in models.storage.all().keys():
            print("** no instance found **")
        else:
            models.storage.all().pop(f"{_r[0]}.{_r[1]}")
            models.storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances
        based on the class name
        """
        _x = arg.split()
        _r = [x.strip() for x in _x]
        if arg:
            if _r[0] not in HBNBCommand.cls_name:
                print("** class doesn't exist **")
                return
        x = [str(obj) for obj in models.storage.all().values()]
        print(x)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""

        _x = arg.split()
        _r = [x.strip() for x in _x]
        _l = len(_r)
        if _l < 1:
            print("** class name missing **")
        elif _r[0] not in HBNBCommand.cls_name:
            print("** class doesn't exist **")
        elif _l < 2:
            print("** instance id missing **")
        elif f"{_r[0]}.{_r[1]}" not in models.storage.all().keys():
            print("** no instance found **")
        elif _l < 3:
            print("** attribute name missing **")
        elif _l < 4:
            print("** value missing **")
        else:
            obj = models.storage.all()[f"{_r[0]}.{_r[1]}"]
            obj.__setattr__(_r[2], _r[3])
            obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
