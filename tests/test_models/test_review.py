#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(own):
        own.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(own):
        own.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(own):
        own.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(own):
        own.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(own):
        own.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(own):
        rv = Review()
        own.assertEqual(str, type(Review.place_id))
        own.assertIn("place_id", dir(rv))
        own.assertNotIn("place_id", rv.__dict__)

    def test_user_id_is_public_class_attribute(own):
        rv = Review()
        own.assertEqual(str, type(Review.user_id))
        own.assertIn("user_id", dir(rv))
        own.assertNotIn("user_id", rv.__dict__)

    def test_text_is_public_class_attribute(own):
        rv = Review()
        own.assertEqual(str, type(Review.text))
        own.assertIn("text", dir(rv))
        own.assertNotIn("text", rv.__dict__)

    def test_two_reviews_unique_ids(own):
        rv1 = Review()
        rv2 = Review()
        own.assertNotEqual(rv1.id, rv2.id)

    def test_two_reviews_different_created_at(own):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        own.assertLess(rv1.created_at, rv2.created_at)

    def test_two_reviews_different_updated_at(own):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        own.assertLess(rv1.updated_at, rv2.updated_at)

    def test_str_representation(own):
        dt = datetime.today()
        dt_repr = repr(dt)
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        rvstr = rv.__str__()
        own.assertIn("[Review] (123456)", rvstr)
        own.assertIn("'id': '123456'", rvstr)
        own.assertIn("'created_at': " + dt_repr, rvstr)
        own.assertIn("'updated_at': " + dt_repr, rvstr)

    def test_args_unused(own):
        rv = Review(None)
        own.assertNotIn(None, rv.__dict__.values())

    def test_instantiation_with_kwargs(own):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        own.assertEqual(rv.id, "345")
        own.assertEqual(rv.created_at, dt)
        own.assertEqual(rv.updated_at, dt)

    def test_instantiation_with_None_kwargs(own):
        with own.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        own.assertLess(first_updated_at, rv.updated_at)

    def test_two_saves(own):
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        second_updated_at = rv.updated_at
        own.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rv.save()
        own.assertLess(second_updated_at, rv.updated_at)

    def test_save_with_arg(own):
        rv = Review()
        with own.assertRaises(TypeError):
            rv.save(None)

    def test_save_updates_file(own):
        rv = Review()
        rv.save()
        rvid = "Review." + rv.id
        with open("file.json", "r") as f:
            own.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(own):
        own.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(own):
        rv = Review()
        own.assertIn("id", rv.to_dict())
        own.assertIn("created_at", rv.to_dict())
        own.assertIn("updated_at", rv.to_dict())
        own.assertIn("__class__", rv.to_dict())

    def test_to_dict_contains_added_attributes(own):
        rv = Review()
        rv.middle_name = "Holberton"
        rv.my_number = 98
        own.assertEqual("Holberton", rv.middle_name)
        own.assertIn("my_number", rv.to_dict())

    def test_to_dict_datetime_attributes_are_strs(own):
        rv = Review()
        rv_dict = rv.to_dict()
        own.assertEqual(str, type(rv_dict["id"]))
        own.assertEqual(str, type(rv_dict["created_at"]))
        own.assertEqual(str, type(rv_dict["updated_at"]))

    def test_to_dict_output(own):
        dt = datetime.today()
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        own.assertDictEqual(rv.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(own):
        rv = Review()
        own.assertNotEqual(rv.to_dict(), rv.__dict__)

    def test_to_dict_with_arg(own):
        rv = Review()
        with own.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
