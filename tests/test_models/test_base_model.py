#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(own):
        own.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(own):
        own.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(own):
        own.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(own):
        own.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(own):
        own.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(own):
        bm1 = BaseModel()
        bm2 = BaseModel()
        own.assertNotEqual(bm1.id, bm2.id)

    def test_two_models_different_created_at(own):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        own.assertLess(bm1.created_at, bm2.created_at)

    def test_two_models_different_updated_at(own):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        own.assertLess(bm1.updated_at, bm2.updated_at)

    def test_str_representation(own):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        own.assertIn("[BaseModel] (123456)", bmstr)
        own.assertIn("'id': '123456'", bmstr)
        own.assertIn("'created_at': " + dt_repr, bmstr)
        own.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_args_unused(own):
        bm = BaseModel(None)
        own.assertNotIn(None, bm.__dict__.values())

    def test_instantiation_with_kwargs(own):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        own.assertEqual(bm.id, "345")
        own.assertEqual(bm.created_at, dt)
        own.assertEqual(bm.updated_at, dt)

    def test_instantiation_with_None_kwargs(own):
        with own.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(own):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        own.assertEqual(bm.id, "345")
        own.assertEqual(bm.created_at, dt)
        own.assertEqual(bm.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

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

    def test_one_save(own):
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        own.assertLess(first_updated_at, bm.updated_at)

    def test_two_saves(own):
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        own.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bm.save()
        own.assertLess(second_updated_at, bm.updated_at)

    def test_save_with_arg(own):
        bm = BaseModel()
        with own.assertRaises(TypeError):
            bm.save(None)

    def test_save_updates_file(own):
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            own.assertIn(bmid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(own):
        bm = BaseModel()
        own.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_contains_correct_keys(own):
        bm = BaseModel()
        own.assertIn("id", bm.to_dict())
        own.assertIn("created_at", bm.to_dict())
        own.assertIn("updated_at", bm.to_dict())
        own.assertIn("__class__", bm.to_dict())

    def test_to_dict_contains_added_attributes(own):
        bm = BaseModel()
        bm.name = "Holberton"
        bm.my_number = 98
        own.assertIn("name", bm.to_dict())
        own.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(own):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        own.assertEqual(str, type(bm_dict["created_at"]))
        own.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(own):
        dt = datetime.today()
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        own.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(own):
        bm = BaseModel()
        own.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_arg(own):
        bm = BaseModel()
        with own.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
