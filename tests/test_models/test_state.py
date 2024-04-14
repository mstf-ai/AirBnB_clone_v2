#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(own):
        own.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(own):
        own.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(own):
        own.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(own):
        own.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(own):
        own.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(own):
        st = State()
        own.assertEqual(str, type(State.name))
        own.assertIn("name", dir(st))
        own.assertNotIn("name", st.__dict__)

    def test_two_states_unique_ids(own):
        st1 = State()
        st2 = State()
        own.assertNotEqual(st1.id, st2.id)

    def test_two_states_different_created_at(own):
        st1 = State()
        sleep(0.05)
        st2 = State()
        own.assertLess(st1.created_at, st2.created_at)

    def test_two_states_different_updated_at(own):
        st1 = State()
        sleep(0.05)
        st2 = State()
        own.assertLess(st1.updated_at, st2.updated_at)

    def test_str_representation(own):
        dt = datetime.today()
        dt_repr = repr(dt)
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        ststr = st.__str__()
        own.assertIn("[State] (123456)", ststr)
        own.assertIn("'id': '123456'", ststr)
        own.assertIn("'created_at': " + dt_repr, ststr)
        own.assertIn("'updated_at': " + dt_repr, ststr)

    def test_args_unused(own):
        st = State(None)
        own.assertNotIn(None, st.__dict__.values())

    def test_instantiation_with_kwargs(own):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        st = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        own.assertEqual(st.id, "345")
        own.assertEqual(st.created_at, dt)
        own.assertEqual(st.updated_at, dt)

    def test_instantiation_with_None_kwargs(own):
        with own.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        own.assertLess(first_updated_at, st.updated_at)

    def test_two_saves(own):
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        second_updated_at = st.updated_at
        own.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        st.save()
        own.assertLess(second_updated_at, st.updated_at)

    def test_save_with_arg(own):
        st = State()
        with own.assertRaises(TypeError):
            st.save(None)

    def test_save_updates_file(own):
        st = State()
        st.save()
        stid = "State." + st.id
        with open("file.json", "r") as f:
            own.assertIn(stid, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(own):
        own.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(own):
        st = State()
        own.assertIn("id", st.to_dict())
        own.assertIn("created_at", st.to_dict())
        own.assertIn("updated_at", st.to_dict())
        own.assertIn("__class__", st.to_dict())

    def test_to_dict_contains_added_attributes(own):
        st = State()
        st.middle_name = "Holberton"
        st.my_number = 98
        own.assertEqual("Holberton", st.middle_name)
        own.assertIn("my_number", st.to_dict())

    def test_to_dict_datetime_attributes_are_strs(own):
        st = State()
        st_dict = st.to_dict()
        own.assertEqual(str, type(st_dict["id"]))
        own.assertEqual(str, type(st_dict["created_at"]))
        own.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(own):
        dt = datetime.today()
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        own.assertDictEqual(st.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(own):
        st = State()
        own.assertNotEqual(st.to_dict(), st.__dict__)

    def test_to_dict_with_arg(own):
        st = State()
        with own.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()
