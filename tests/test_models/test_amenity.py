#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(own):
        own.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(own):
        own.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(own):
        own.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(own):
        own.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(own):
        own.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(own):
        am = Amenity()
        own.assertEqual(str, type(Amenity.name))
        own.assertIn("name", dir(Amenity()))
        own.assertNotIn("name", am.__dict__)

    def test_two_amenities_unique_ids(own):
        am1 = Amenity()
        am2 = Amenity()
        own.assertNotEqual(am1.id, am2.id)

    def test_two_amenities_different_created_at(own):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        own.assertLess(am1.created_at, am2.created_at)

    def test_two_amenities_different_updated_at(own):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        own.assertLess(am1.updated_at, am2.updated_at)

    def test_str_representation(own):
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        amstr = am.__str__()
        own.assertIn("[Amenity] (123456)", amstr)
        own.assertIn("'id': '123456'", amstr)
        own.assertIn("'created_at': " + dt_repr, amstr)
        own.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(own):
        am = Amenity(None)
        own.assertNotIn(None, am.__dict__.values())

    def test_instantiation_with_kwargs(own):
        """instantiation with kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        own.assertEqual(am.id, "345")
        own.assertEqual(am.created_at, dt)
        own.assertEqual(am.updated_at, dt)

    def test_instantiation_with_None_kwargs(own):
        with own.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(own):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        own.assertLess(first_updated_at, am.updated_at)

    def test_two_saves(own):
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        own.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        am.save()
        own.assertLess(second_updated_at, am.updated_at)

    def test_save_with_arg(own):
        am = Amenity()
        with own.assertRaises(TypeError):
            am.save(None)

    def test_save_updates_file(own):
        am = Amenity()
        am.save()
        amid = "Amenity." + am.id
        with open("file.json", "r") as f:
            own.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(own):
        own.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(own):
        am = Amenity()
        own.assertIn("id", am.to_dict())
        own.assertIn("created_at", am.to_dict())
        own.assertIn("updated_at", am.to_dict())
        own.assertIn("__class__", am.to_dict())

    def test_to_dict_contains_added_attributes(own):
        am = Amenity()
        am.middle_name = "Holberton"
        am.my_number = 98
        own.assertEqual("Holberton", am.middle_name)
        own.assertIn("my_number", am.to_dict())

    def test_to_dict_datetime_attributes_are_strs(own):
        am = Amenity()
        am_dict = am.to_dict()
        own.assertEqual(str, type(am_dict["id"]))
        own.assertEqual(str, type(am_dict["created_at"]))
        own.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(own):
        dt = datetime.today()
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        own.assertDictEqual(am.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(own):
        am = Amenity()
        own.assertNotEqual(am.to_dict(), am.__dict__)

    def test_to_dict_with_arg(own):
        am = Amenity()
        with own.assertRaises(TypeError):
            am.to_dict(None)


if __name__ == "__main__":
    unittest.main()
