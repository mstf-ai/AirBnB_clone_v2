#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompting(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def test_prompt_string(own):
        own.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(""))
            own.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter."""

    def test_help_quit(own):
        h = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help quit"))
            own.assertEqual(h, output.getvalue().strip())

    def test_help_create(own):
        h = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help create"))
            own.assertEqual(h, output.getvalue().strip())

    def test_help_EOF(own):
        h = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help EOF"))
            own.assertEqual(h, output.getvalue().strip())

    def test_help_show(own):
        h = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help show"))
            own.assertEqual(h, output.getvalue().strip())

    def test_help_destroy(own):
        h = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help destroy"))
            own.assertEqual(h, output.getvalue().strip())

    def test_help_all(own):
        h = ("Usage: all or all <class> or <class>.all()\n        "
             "Display string representations of all instances of a given class"
             ".\n        If no class is specified, displays all instantiated "
             "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help all"))
            own.assertEqual(h, output.getvalue().strip())

    def test_help_count(own):
        h = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help count"))
            own.assertEqual(h, output.getvalue().strip())

    def test_help_update(own):
        h = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
             "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
             ">) or\n       <class>.update(<id>, <dictionary>)\n        "
             "Update a class instance of a given id by adding or updating\n   "
             "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help update"))
            own.assertEqual(h, output.getvalue().strip())

    def test_help(own):
        h = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("help"))
            own.assertEqual(h, output.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(own):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.obj = {}

    @classmethod
    def tearDown(own):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(own):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_class(own):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create MyModel"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_syntax(own):
        correct = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            own.assertEqual(correct, output.getvalue().strip())
        correct = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_create_object(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            own.assertLess(0, len(output.getvalue().strip()))
            testKey = "BaseModel.{}".format(output.getvalue().strip())
            own.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create User"))
            own.assertLess(0, len(output.getvalue().strip()))
            testKey = "User.{}".format(output.getvalue().strip())
            own.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create State"))
            own.assertLess(0, len(output.getvalue().strip()))
            testKey = "State.{}".format(output.getvalue().strip())
            own.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create City"))
            own.assertLess(0, len(output.getvalue().strip()))
            testKey = "City.{}".format(output.getvalue().strip())
            own.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            own.assertLess(0, len(output.getvalue().strip()))
            testKey = "Amenity.{}".format(output.getvalue().strip())
            own.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            own.assertLess(0, len(output.getvalue().strip()))
            testKey = "Place.{}".format(output.getvalue().strip())
            own.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Review"))
            own.assertLess(0, len(output.getvalue().strip()))
            testKey = "Review.{}".format(output.getvalue().strip())
            own.assertIn(testKey, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def setUp(own):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.obj = {}

    @classmethod
    def tearDown(own):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missing_class(own):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(".show()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_show_invalid_class(own):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show MyModel"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_space_notation(own):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show User"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show State"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show City"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show Amenity"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show Place"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show Review"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_dot_notation(own):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("User.show()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("State.show()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("City.show()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Place.show()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Review.show()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_space_notation(own):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show User 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show State 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show City 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show Place 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("show Review 1"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_dot_notation(own):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_show_objects_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "show BaseModel {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create User"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create State"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create City"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_objects_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.show({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create User"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(testID)]
            command = "User.show({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create State"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(testID)]
            command = "State.show({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(testID)]
            command = "Place.show({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create City"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(testID)]
            command = "City.show({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "Amenity.show({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(testID)]
            command = "Review.show({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Unittests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def setUp(own):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.obj = {}

    @classmethod
    def tearDown(own):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def test_destroy_missing_class(own):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(".destroy()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_class(own):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_destroy_id_missing_space_notation(own):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy User"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy State"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy City"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy Place"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy Review"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_destroy_id_missing_dot_notation(own):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_id_space_notation(own):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(own):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_destroy_objects_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "destroy BaseModel {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create User"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create State"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create City"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())

    def test_destroy_objects_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.destroy({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create User"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(testID)]
            command = "User.destroy({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create State"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(testID)]
            command = "State.destroy({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(testID)]
            command = "Place.destroy({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create City"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(testID)]
            command = "City.destroy({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "Amenity.destroy({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(testID)]
            command = "Review.destory({})".format(testID)
            own.assertFalse(HBNBCommand().onecmd(command))
            own.assertNotIn(obj, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

    @classmethod
    def setUp(own):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.obj = {}

    @classmethod
    def tearDown(own):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_all_invalid_class(own):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all MyModel"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_all_objects_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            own.assertFalse(HBNBCommand().onecmd("create User"))
            own.assertFalse(HBNBCommand().onecmd("create State"))
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            own.assertFalse(HBNBCommand().onecmd("create City"))
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            own.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all"))
            own.assertIn("BaseModel", output.getvalue().strip())
            own.assertIn("User", output.getvalue().strip())
            own.assertIn("State", output.getvalue().strip())
            own.assertIn("Place", output.getvalue().strip())
            own.assertIn("City", output.getvalue().strip())
            own.assertIn("Amenity", output.getvalue().strip())
            own.assertIn("Review", output.getvalue().strip())

    def test_all_objects_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            own.assertFalse(HBNBCommand().onecmd("create User"))
            own.assertFalse(HBNBCommand().onecmd("create State"))
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            own.assertFalse(HBNBCommand().onecmd("create City"))
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            own.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(".all()"))
            own.assertIn("BaseModel", output.getvalue().strip())
            own.assertIn("User", output.getvalue().strip())
            own.assertIn("State", output.getvalue().strip())
            own.assertIn("Place", output.getvalue().strip())
            own.assertIn("City", output.getvalue().strip())
            own.assertIn("Amenity", output.getvalue().strip())
            own.assertIn("Review", output.getvalue().strip())

    def test_all_single_object_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            own.assertFalse(HBNBCommand().onecmd("create User"))
            own.assertFalse(HBNBCommand().onecmd("create State"))
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            own.assertFalse(HBNBCommand().onecmd("create City"))
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            own.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            own.assertIn("BaseModel", output.getvalue().strip())
            own.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all User"))
            own.assertIn("User", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all State"))
            own.assertIn("State", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all City"))
            own.assertIn("City", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all Amenity"))
            own.assertIn("Amenity", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all Place"))
            own.assertIn("Place", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("all Review"))
            own.assertIn("Review", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())

    def test_all_single_object_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            own.assertFalse(HBNBCommand().onecmd("create User"))
            own.assertFalse(HBNBCommand().onecmd("create State"))
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            own.assertFalse(HBNBCommand().onecmd("create City"))
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            own.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            own.assertIn("BaseModel", output.getvalue().strip())
            own.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("User.all()"))
            own.assertIn("User", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("State.all()"))
            own.assertIn("State", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("City.all()"))
            own.assertIn("City", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            own.assertIn("Amenity", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Place.all()"))
            own.assertIn("Place", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Review.all()"))
            own.assertIn("Review", output.getvalue().strip())
            own.assertNotIn("BaseModel", output.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUp(own):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.obj = {}

    @classmethod
    def tearDown(own):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_missing_class(own):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(".update()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_class(own):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update MyModel"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_id_space_notation(own):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update User"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update State"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update City"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update Amenity"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update Place"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update Review"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_id_dot_notation(own):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("User.update()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("State.update()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("City.update()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Place.update()"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Review.update()"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_id_space_notation(own):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update User 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update State 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update City 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update Place 1"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("update Review 1"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_id_dot_notation(own):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_name_space_notation(own):
        correct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = output.getvalue().strip()
            testCmd = "update BaseModel {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create User"))
            testId = output.getvalue().strip()
            testCmd = "update User {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create State"))
            testId = output.getvalue().strip()
            testCmd = "update State {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create City"))
            testId = output.getvalue().strip()
            testCmd = "update City {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = output.getvalue().strip()
            testCmd = "update Amenity {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = output.getvalue().strip()
            testCmd = "update Place {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(own):
        correct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = output.getvalue().strip()
            testCmd = "BaseModel.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create User"))
            testId = output.getvalue().strip()
            testCmd = "User.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create State"))
            testId = output.getvalue().strip()
            testCmd = "State.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create City"))
            testId = output.getvalue().strip()
            testCmd = "City.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = output.getvalue().strip()
            testCmd = "Amenity.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = output.getvalue().strip()
            testCmd = "Place.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_value_space_notation(own):
        correct = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "update BaseModel {} attr_name".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "update User {} attr_name".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "update State {} attr_name".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "update City {} attr_name".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "update Amenity {} attr_name".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "update Place {} attr_name".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "update Review {} attr_name".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_value_dot_notation(own):
        correct = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "BaseModel.update({}, attr_name)".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "User.update({}, attr_name)".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "State.update({}, attr_name)".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "City.update({}, attr_name)".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "Amenity.update({}, attr_name)".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "Place.update({}, attr_name)".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            testCmd = "Review.update({}, attr_name)".format(testId)
            own.assertFalse(HBNBCommand().onecmd(testCmd))
            own.assertEqual(correct, output.getvalue().strip())

    def test_update_valid_string_attr_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        testCmd = "update BaseModel {} attr_name 'attr_value'".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        testCmd = "update User {} attr_name 'attr_value'".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        testCmd = "update State {} attr_name 'attr_value'".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        testCmd = "update City {} attr_name 'attr_value'".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} attr_name 'attr_value'".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        testCmd = "update Amenity {} attr_name 'attr_value'".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        testCmd = "update Review {} attr_name 'attr_value'".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        own.assertTrue("attr_value", test_dict["attr_name"])

    def test_update_valid_string_attr_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tId = output.getvalue().strip()
        testCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tId = output.getvalue().strip()
        testCmd = "User.update({}, attr_name, 'attr_value')".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(tId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tId = output.getvalue().strip()
        testCmd = "State.update({}, attr_name, 'attr_value')".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["State.{}".format(tId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tId = output.getvalue().strip()
        testCmd = "City.update({}, attr_name, 'attr_value')".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["City.{}".format(tId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        testCmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tId = output.getvalue().strip()
        testCmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tId = output.getvalue().strip()
        testCmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Review.{}".format(tId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_int_attr_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} max_guest 98".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_int_attr_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        testCmd = "Place.update({}, max_guest, 98)".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        own.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_float_attr_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} latitude 7.2".format(testId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_float_attr_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        testCmd = "Place.update({}, latitude, 7.2)".format(tId)
        own.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        own.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_dictionary_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        testCmd = "update BaseModel {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        testCmd = "update User {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        testCmd = "update State {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        testCmd = "update City {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        testCmd = "update Amenity {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        testCmd = "update Review {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        testCmd = "BaseModel.update({}".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        testCmd = "User.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        testCmd = "State.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        testCmd = "City.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        testCmd = "Amenity.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        testCmd = "Review.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        own.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual(9.8, test_dict["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(own):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        own.assertEqual(9.8, test_dict["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def setUp(own):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(own):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_invalid_class(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            own.assertEqual("0", output.getvalue().strip())

    def test_count_object(own):
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            own.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("User.count()"))
            own.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("State.count()"))
            own.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Place.count()"))
            own.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("City.count()"))
            own.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            own.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            own.assertFalse(HBNBCommand().onecmd("Review.count()"))
            own.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
