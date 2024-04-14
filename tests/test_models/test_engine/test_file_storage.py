#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(own):
        own.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(own):
        with own.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(own):
        own.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(own):
        own.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(own):
        own.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(own):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        FileStorage._FileStorage__objects = {}

    def test_all(own):
        own.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(own):
        with own.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(own):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        own.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        own.assertIn(bm, models.storage.all().values())
        own.assertIn("User." + us.id, models.storage.all().keys())
        own.assertIn(us, models.storage.all().values())
        own.assertIn("State." + st.id, models.storage.all().keys())
        own.assertIn(st, models.storage.all().values())
        own.assertIn("Place." + pl.id, models.storage.all().keys())
        own.assertIn(pl, models.storage.all().values())
        own.assertIn("City." + cy.id, models.storage.all().keys())
        own.assertIn(cy, models.storage.all().values())
        own.assertIn("Amenity." + am.id, models.storage.all().keys())
        own.assertIn(am, models.storage.all().values())
        own.assertIn("Review." + rv.id, models.storage.all().keys())
        own.assertIn(rv, models.storage.all().values())

    def test_new_with_args(own):
        with own.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(own):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            own.assertIn("BaseModel." + bm.id, save_text)
            own.assertIn("User." + us.id, save_text)
            own.assertIn("State." + st.id, save_text)
            own.assertIn("Place." + pl.id, save_text)
            own.assertIn("City." + cy.id, save_text)
            own.assertIn("Amenity." + am.id, save_text)
            own.assertIn("Review." + rv.id, save_text)

    def test_save_with_arg(own):
        with own.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(own):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        own.assertIn("BaseModel." + bm.id, objs)
        own.assertIn("User." + us.id, objs)
        own.assertIn("State." + st.id, objs)
        own.assertIn("Place." + pl.id, objs)
        own.assertIn("City." + cy.id, objs)
        own.assertIn("Amenity." + am.id, objs)
        own.assertIn("Review." + rv.id, objs)

    def test_reload_with_arg(own):
        with own.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
