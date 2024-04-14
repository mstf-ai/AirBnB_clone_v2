#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(own):
        own.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(own):
        own.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(own):
        own.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(own):
        own.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(own):
        own.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(str, type(Place.city_id))
        own.assertIn("city_id", dir(pl))
        own.assertNotIn("city_id", pl.__dict__)

    def test_user_id_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(str, type(Place.user_id))
        own.assertIn("user_id", dir(pl))
        own.assertNotIn("user_id", pl.__dict__)

    def test_name_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(str, type(Place.name))
        own.assertIn("name", dir(pl))
        own.assertNotIn("name", pl.__dict__)

    def test_description_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(str, type(Place.description))
        own.assertIn("description", dir(pl))
        own.assertNotIn("desctiption", pl.__dict__)

    def test_number_rooms_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(int, type(Place.number_rooms))
        own.assertIn("number_rooms", dir(pl))
        own.assertNotIn("number_rooms", pl.__dict__)

    def test_number_bathrooms_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(int, type(Place.number_bathrooms))
        own.assertIn("number_bathrooms", dir(pl))
        own.assertNotIn("number_bathrooms", pl.__dict__)

    def test_max_guest_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(int, type(Place.max_guest))
        own.assertIn("max_guest", dir(pl))
        own.assertNotIn("max_guest", pl.__dict__)

    def test_price_by_night_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(int, type(Place.price_by_night))
        own.assertIn("price_by_night", dir(pl))
        own.assertNotIn("price_by_night", pl.__dict__)

    def test_latitude_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(float, type(Place.latitude))
        own.assertIn("latitude", dir(pl))
        own.assertNotIn("latitude", pl.__dict__)

    def test_longitude_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(float, type(Place.longitude))
        own.assertIn("longitude", dir(pl))
        own.assertNotIn("longitude", pl.__dict__)

    def test_amenity_ids_is_public_class_attribute(own):
        pl = Place()
        own.assertEqual(list, type(Place.amenity_ids))
        own.assertIn("amenity_ids", dir(pl))
        own.assertNotIn("amenity_ids", pl.__dict__)

    def test_two_places_unique_ids(own):
        pl1 = Place()
        pl2 = Place()
        own.assertNotEqual(pl1.id, pl2.id)

    def test_two_places_different_created_at(own):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        own.assertLess(pl1.created_at, pl2.created_at)

    def test_two_places_different_updated_at(own):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        own.assertLess(pl1.updated_at, pl2.updated_at)

    def test_str_representation(own):
        dt = datetime.today()
        dt_repr = repr(dt)
        pl = Place()
        pl.id = "123456"
        pl.created_at = pl.updated_at = dt
        plstr = pl.__str__()
        own.assertIn("[Place] (123456)", plstr)
        own.assertIn("'id': '123456'", plstr)
        own.assertIn("'created_at': " + dt_repr, plstr)
        own.assertIn("'updated_at': " + dt_repr, plstr)

    def test_args_unused(own):
        pl = Place(None)
        own.assertNotIn(None, pl.__dict__.values())

    def test_instantiation_with_kwargs(own):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        pl = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        own.assertEqual(pl.id, "345")
        own.assertEqual(pl.created_at, dt)
        own.assertEqual(pl.updated_at, dt)

    def test_instantiation_with_None_kwargs(own):
        with own.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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
        pl = Place()
        sleep(0.05)
        first_updated_at = pl.updated_at
        pl.save()
        own.assertLess(first_updated_at, pl.updated_at)

    def test_two_saves(own):
        pl = Place()
        sleep(0.05)
        first_updated_at = pl.updated_at
        pl.save()
        second_updated_at = pl.updated_at
        own.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        pl.save()
        own.assertLess(second_updated_at, pl.updated_at)

    def test_save_with_arg(own):
        pl = Place()
        with own.assertRaises(TypeError):
            pl.save(None)

    def test_save_updates_file(own):
        pl = Place()
        pl.save()
        plid = "Place." + pl.id
        with open("file.json", "r") as f:
            own.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(own):
        own.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(own):
        pl = Place()
        own.assertIn("id", pl.to_dict())
        own.assertIn("created_at", pl.to_dict())
        own.assertIn("updated_at", pl.to_dict())
        own.assertIn("__class__", pl.to_dict())

    def test_to_dict_contains_added_attributes(own):
        pl = Place()
        pl.middle_name = "Holberton"
        pl.my_number = 98
        own.assertEqual("Holberton", pl.middle_name)
        own.assertIn("my_number", pl.to_dict())

    def test_to_dict_datetime_attributes_are_strs(own):
        pl = Place()
        pl_dict = pl.to_dict()
        own.assertEqual(str, type(pl_dict["id"]))
        own.assertEqual(str, type(pl_dict["created_at"]))
        own.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(own):
        dt = datetime.today()
        pl = Place()
        pl.id = "123456"
        pl.created_at = pl.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        own.assertDictEqual(pl.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(own):
        pl = Place()
        own.assertNotEqual(pl.to_dict(), pl.__dict__)

    def test_to_dict_with_arg(own):
        pl = Place()
        with own.assertRaises(TypeError):
            pl.to_dict(None)


if __name__ == "__main__":
    unittest.main()
