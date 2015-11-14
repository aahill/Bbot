from unittest import TestCase
from ..PinAndPinGroup import *
#from PinAndPinGroup import *
from nose import *
from nose.tools import *
from collections import defaultdict

class TestPin(TestCase):

    def test_setAvailability(self):
        testPin = Pin('test', 5, '')
        testPin.setAvailability(False)
        if testPin.available:
            self.fail()


"""
contains the pin groups and number of inputs and outputs
"""
class PinGroupData:
    def __init__(self, group, num_inputs, num_outputs):
        self.group = group
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

num_pin_groups = 14

"""
Using an index, return a new pin group, with acompanying input/output numbers
"""


def generate_pin_group(group_index):
    return{
        0: PinGroupData(Group1(), 7, 4),
        1: PinGroupData(Group2(), 7, 4),
        2: PinGroupData(Group3(), 7, 8),
        3: PinGroupData(Group4(), 7, 8),
        4: PinGroupData(Group3(), 7, 8),
        5: PinGroupData(Group3(), 7, 8),
        6: PinGroupData(GroupPl(), 6, 6),
        7: PinGroupData(GroupPr(), 6, 6),
        8: PinGroupData(GroupRl(), 6, 6),
        9: PinGroupData(GroupRr(), 6, 6),
        10: PinGroupData(GroupBl(), 4, 4),
        11: PinGroupData(GroupBr(), 4, 4),
        12: PinGroupData(GroupFr(), 4, 4),
        13: PinGroupData(GroupFl(), 4, 4)
    }[group_index]


"""
test cases for get input methods of the pin groups
"""


def test_get_input():
    for x in range(num_pin_groups):

        yield getInput_trial, x

"""
ensure group 2 contains the expected number of input pins
"""


def test_get_output():
    for x in range(num_pin_groups):
        yield getOutput_trial, x


"""
ensure the get_random_input function returns the correct number of unique pins
"""


def test_get_random_input():
    for x in range(num_pin_groups):
            yield get_random_input_trial, x


"""
ensure the get_random_output function returns the correct number of unique pins
"""
def test_get_random_output():
    for x in range(num_pin_groups):
            yield get_random_output_trial, x


        # """
        # ensure the get_random_input function returns the correct number of unique pins
        # """
        # def test_get_random_output(self):
        #     returned_pins = []
        #     for x in range(self.number_of_outputs):
        #         rand_pin = self.group2.get_random_output()
        #         returned_pins.append(rand_pin)
        #     """
        #     'flatten' the list so that it contains only unique pins.
        #     When compared to the original list, if there are duplicate pins in the flattened list,
        #     its length will be less than the original.
        #     """
        #     if len(set(returned_pins)) != len(returned_pins):
        #         self.fail('Group 2 random_input returned duplicate pins!')

def getInput_trial(index):
    test_group_info = generate_pin_group(index)
    group = test_group_info.group
    num_of_inputs = test_group_info.num_inputs
    returned_pins = []
    for x in range(num_of_inputs):
        returned_pins.append(group.get_input(x))
    assert_equal(len(returned_pins), num_of_inputs)
    assert_true(all_unique_pins(returned_pins))


def getOutput_trial(index):
    test_group_info = generate_pin_group(index)
    group = test_group_info.group
    num_of_outputs = test_group_info.num_outputs
    taken_pins = []
    for x in range(num_of_outputs):
        taken_pins.append(group.get_output(x))
    assert_equal(len(taken_pins), num_of_outputs)
    assert_true(all_unique_pins(taken_pins))


def get_random_input_trial(index):
    group_info = generate_pin_group(index)
    returned_pins = []
    for x in range(group_info.num_inputs):
        rand_pin = group_info.group.get_random_input()
        returned_pins.append(rand_pin)
    """
    'flatten' the list so that it contains only unique pins.
    When compared to the original list, if there are duplicate pins in the flattened list,
    its length will be less than the original.
    """
    #assert_equal(len(set(returned_pins)), len(returned_pins))
    assert_true(all_unique_pins(returned_pins))


def get_random_output_trial(index):
    group_info = generate_pin_group(index)
    returned_pins = []
    for x in range(group_info.num_outputs):
        rand_pin = group_info.group.get_random_output()
        returned_pins.append(rand_pin)
    """
    'flatten' the list so that it contains only unique pins.
    When compared to the original list, if there are duplicate pins in the flattened list,
    its length will be less than the original.
    """
    #assert_equal(len(set(returned_pins)), len(returned_pins))
    assert_true(all_unique_pins(returned_pins))

"""
determines if all the pins in a list are unique
"""
def all_unique_pins(list_of_pins):
    pin_tuples = []
    for pin in list_of_pins:
        pin_tuples.append((pin.group_id, pin.number))  # get pin id and pin number

    pin_dict = defaultdict(list)  # create hashmap to store pin numbers with their pin_ids
    for pin_id, pin_num in pin_tuples:
        pin_dict[pin_id].append(pin_num)

    for hashed_pins in pin_dict.items():
        if len(set(hashed_pins[1])) == len(hashed_pins[1]):
            return True
    return False


# create dictionary, check that one key corresponds to exactly one value