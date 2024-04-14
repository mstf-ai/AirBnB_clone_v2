#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(own):
        own.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(own):
        own.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(own):
        own.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(own):
        own.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(own):
        own.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(own):
        cy = City()
        own.assertEqual(str, type(City.state_id))
        own.assertIn("state_id", dir(cy))
        own.assertNotIn("state_id", cy.__dict__)

    def test_name_is_public_class_attribute(own):
        cy = City()
        own.assertEqual(str, type(City.name))
        own.assertIn("name", dir(cy))
        own.assertNotIn("name", cy.__dict__)

    def test_two_cities_unique_ids(own):
        cy1 = City()
        cy2 = City()
        own.assertNotEqual(cy1.id, cy2.id)

    def test_two_cities_different_created_at(own):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        own.assertLess(cy1.created_at, cy2.created_at)

    def test_two_cities_different_updated_at(own):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        own.assertLess(cy1.updated_at, cy2.updated_at)

    def test_str_representation(own):
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cystr = cy.__str__()
        own.assertIn("[City] (123456)", cystr)
        own.assertIn("'id': '123456'", cystr)
        own.assertIn("'created_at': " + dt_repr, cystr)
        own.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_unused(own):
        cy = City(None)
        own.assertNotIn(None, cy.__dict__.values())

    def test_instantiation_with_kwargs(own):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        own.assertEqual(cy.id, "345")
        own.assertEqual(cy.created_at, dt)
        own.assertEqual(cy.updated_at, dt)

    def test_instantiation_with_None_kwargs(own):
        with own.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        own.assertLess(first_updated_at, cy.updated_at)

    def test_two_saves(own):
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        own.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cy.save()
        own.assertLess(second_updated_at, cy.updated_at)

    def test_save_with_arg(own):
        cy = City()
        with own.assertRaises(TypeError):
            cy.save(None)

    def test_save_updates_file(own):
        cy = City()
        cy.save()
        cyid = "City." + cy.id
        with open("file.json", "r") as f:
            own.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(own):
        own.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(own):
        cy = City()
        own.assertIn("id", cy.to_dict())
        own.assertIn("created_at", cy.to_dict())
        own.assertIn("updated_at", cy.to_dict())
        own.assertIn("__class__", cy.to_dict())

    def test_to_dict_contains_added_attributes(own):
        cy = City()
        cy.middle_name = "Holberton"
        cy.my_number = 98
        own.assertEqual("Holberton", cy.middle_name)
        own.assertIn("my_number", cy.to_dict())

    def test_to_dict_datetime_attributes_are_strs(own):
        cy = City()
        cy_dict = cy.to_dict()
        own.assertEqual(str, type(cy_dict["id"]))
        own.assertEqual(str, type(cy_dict["created_at"]))
        own.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(own):
        dt = datetime.today()
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        own.assertDictEqual(cy.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(own):
        cy = City()
        own.assertNotEqual(cy.to_dict(), cy.__dict__)

    def test_to_dict_with_arg(own):
        cy = City()
        with own.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
