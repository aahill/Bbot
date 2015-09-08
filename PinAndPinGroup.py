
import random

class pin:
    # group_id represents the group the pin belongs to
    # number identifies the pin number within the group
    def __init__(self, group_id, number, group):
        self.group_id = group_id
        self.number = number
        #self.group = group
        self.available = True

    def setAvailability(self, bool):
        self.available = bool



class PinGroup(object):
    def __call__(self):
        return self
        
    def __init__(self):
        self.type = None

    def get_input(self, pin_index):
        raise NotImplementedError

    def get_output(self, pin_index):
        raise NotImplementedError

    def get_random_input(self):
        raise NotImplementedError

    def get_random_output(self):
        raise NotImplementedError

    def match_and_remove_pin(self, pin, pin_list1, pin_list2=None):
        pin_found = False
        for x in range(len(pin_list1)):
            if pin.group_id == pin_list1[x].group_id and pin.number == pin_list1[x].number:
                pin_found = True
                # NOTE: instead of deleting the pin from the list, the pin's available variable will be set to false.
                # this allows for the ability to determine if a pin is 'taken' by another thread
                pin_list1[x].setAvailability(False)
                break
    
        if not pin_found and pin_list2 is not None:
            for x in range(len(pin_list2)):
                # None types in the pin list signify pins that are no longer available, and should be skipped over
                if pin_list2[x] is not None:
                    if pin.group_id == pin_list2[x].group_id and pin.number == pin_list2[x].number:
                        pin_found = True
                        # NOTE: instead of deleting the pin from the list, the pin's available variable will be set to false.
                        # this allows for the ability to determine if a pin is 'taken' by another thread
                        pin_list2[x].setAvailability(False)
                        break
        if pin_found is False:
            pass
        assert pin_found is True
    
    
    #NOTE: I(nhibitory) and E(xcitatory) are inputs
        # N and T(hreshold) are outputs
    



class MotorSensorPinGroup(PinGroup):
    def __init__(self):
        #PinGroup.__init__(self)
        super(PinGroup, self).__init__()
        self.pins = None

    def get_input(self, pin_index):
        target_pin = self.pins[pin_index]
        #print target_pin
        #self.match_and_remove(target_pin, self.pins)
        if target_pin.available == False:
            raise IndexError
        else:
            self.call_match_and_remove_pin(target_pin, self.pins)
        return target_pin

    def get_output(self, pin_index):
        target_pin = self.pins[pin_index]
        #self.match_and_remove(target_pin, self.pins)
        if target_pin.available ==False:
            raise IndexError
        else:
            self.call_match_and_remove_pin(target_pin, self.pins)
        return target_pin

    def get_random_input(self):
        target_pin = random.choice([pin for pin in self.pins if pin.available is True])
        #self.match_and_remove(target_pin, self.pins)
        self.call_match_and_remove_pin(target_pin, self.pins)
        return target_pin

    def get_random_output(self):
        target_pin = random.choice([pin for pin in self.pins if pin.available is True])
        #self.match_and_remove(target_pin, self.pins)
        self.call_match_and_remove_pin(target_pin, self.pins)
        return target_pin

    def call_match_and_remove_pin(self, pin, pin_list1, pin_list2=None):
        super(MotorSensorPinGroup, self).match_and_remove_pin(pin, pin_list1, pin_list2)


class Group1(PinGroup):
    def __init__(self):
        #PinGroup.__init__(self)
        super(PinGroup, self).__init__()
        self.type = "standard"
        # list of available pins in group e1
        self.e1 = [Pin("e1", i, self) for i in range(4)]
        self.i1 = [Pin("i2", i, self) for i in range(3)]
        self.n1 = [Pin("n1", i, self) for i in range(4)]

    def get_input(self, pin_index):
        all_inputs = self.e1 + self.i1
        target_pin = all_inputs[pin_index]
        target_pin.available = False
        #self.match_and_remove(target_pin, self.e1, self.i1)
        self.call_match_and_remove_pin(target_pin, self.e1, self.i1)
        return target_pin

    def get_output(self, pin_index):
        target_pin = self.n1[pin_index]
        #self.match_and_remove(target_pin, self.n1)
        self.call_match_and_remove_pin(target_pin, self.n1)
        return target_pin

    """
    gets a random available input pin
    """
    def get_random_input(self):
        # put all available pins in a list
        available_inputs = [pin for pin in self.e1 + self.i1 if pin.available is True]
        target_pin = random.choice(available_inputs)
        self.call_match_and_remove_pin(target_pin, self.e1, self.i1)
        return target_pin

    def get_random_output(self):
        # put all available pins in a list
        target_pin = random.choice([pin for pin in self.n1 if pin.available is True])
        self.call_match_and_remove_pin(target_pin, self.n1)
        return target_pin

    def call_match_and_remove_pin(self, pin, pin_list1, pin_list2=None):
        super(Group1, self).match_and_remove_pin(pin, pin_list1, pin_list2)



class Group3(PinGroup):
    def __init__(self):
        super(PinGroup, self).__init__()
        self.type = "standard"
        # list of available pins in group 3
        self.e3 = [Pin("e3", i, self) for i in range(4)]
        self.i3 = [Pin("i3", i, self) for i in range(3)]
        self.t3 = [Pin("t3", i, self) for i in range(4)]
        self.n3 = [Pin("n3", i, self) for i in range(4)]

    def get_input(self, pin_index):
        all_inputs = self.e3 + self.i3
        target_pin = all_inputs[pin_index]
        self.call_match_and_remove_pin(target_pin, self.e3, self.i3)
        return target_pin

    def get_output(self, pin_index):
        all_outputs = self.n3 + self.t3
        target_pin = all_outputs[pin_index]
        self.call_match_and_remove_pin(target_pin, self.n3, self.t3)
        return target_pin

    """
    returns a random available input
    """
    def get_random_input(self):
        available_inputs = [pin for pin in self.e3 + self.i3 if pin.available is True]
        target_pin = random.choice(available_inputs)
        self.call_match_and_remove_pin(target_pin, self.e3, self.i3)
        return target_pin

    """
    returns a random available input
    """
    def get_random_output(self):
        available_outputs = [pin for pin in self.n3 + self.t3 if pin.available is True]
        target_pin = random.choice(available_outputs)
        self.call_match_and_remove_pin(target_pin, self.n3, self.t3)
        return target_pin

    def call_match_and_remove_pin(self, pin, pin_list1, pin_list2=None):
        super(Group3, self).match_and_remove_pin(pin, pin_list1, pin_list2)

class Group4(PinGroup):
    def __init__(self):
        #PinGroup.__init__(self)
        super(PinGroup, self).__init__()
        self.type = "standard"
        # list of available pins in group 4
        self.e4 = [Pin("e4", i, self) for i in range(4)]
        self.i4 = [Pin("i4", i, self) for i in range(3)]
        self.t4 = [Pin("t4", i, self) for i in range(4)]
        self.n4 = [Pin("n4", i, self) for i in range(4)]

    def get_input(self, pin_index):
        all_inputs = self.e4 + self.i4
        target_pin = all_inputs[pin_index]
        #self.match_and_remove(target_pin, self.e4, self.i4)
        self.call_match_and_remove_pin(target_pin, self.e4, self.i4)
        return target_pin

    def get_output(self, pin_index):
        all_outputs = self.n4 + self.t4
        target_pin = all_outputs[pin_index]
        #self.match_and_remove(target_pin, self.n4, self.t4)
        self.call_match_and_remove_pin(target_pin, self.n4, self.t4)
        return target_pin

    """
    returns a random available input
    """
    def get_random_input(self):
        available_inputs = [pin for pin in self.e4 + self.i4 if pin.available is True]
        target_pin = random.choice(available_inputs)
        self.call_match_and_remove_pin(target_pin, self.e4, self.i4)
        return target_pin

    """
    returns a random available input
    """
    def get_random_output(self):
        available_outputs = [pin for pin in self.n4 + self.t4 if pin.available is True]
        target_pin = random.choice(available_outputs)
        self.call_match_and_remove_pin(target_pin, self.n4, self.t4)
        return target_pin

    def call_match_and_remove_pin(self, pin, pin_list1, pin_list2=None):
        super(Group4, self).match_and_remove_pin(pin, pin_list1, pin_list2)



class Group5(PinGroup):
    def __init__(self):
        #PinGroup.__init__(self)
        super(PinGroup, self).__init__()
        self.type = "standard"
        # list of available pins in group 5
        self.e5 = [Pin("e5", i, self) for i in range(4)]
        self.i5 = [Pin("i5", i, self) for i in range(3)]
        self.t5 = [Pin("t5", i, self) for i in range(4)]
        self.n5 = [Pin("n5", i, self) for i in range(4)]

    def get_input(self, pin_index):
        all_inputs = self.e5 + self.i5
        target_pin = all_inputs[pin_index]
        #self.match_and_remove(target_pin, self.e5, self.i5)
        self.call_match_and_remove_pin(target_pin, self.e5, self.i5)
        return target_pin

    def get_output(self, pin_index):
        all_outputs = self.n5 + self.t5
        target_pin = all_outputs[pin_index]
        self.call_match_and_remove_pin(target_pin, self.n5, self.t5)
        #self.match_and_remove(target_pin, self.n5, self.t5)
        return target_pin

    """
    returns a random available input
    """
    def get_random_input(self):
        available_inputs = [pin for pin in self.e5 + self.i5 if pin.available is True]
        target_pin = random.choice(available_inputs)
        self.call_match_and_remove_pin(target_pin, self.e5, self.i5)
        return target_pin

    """
    returns a random available input
    """
    def get_random_output(self):
        available_outputs = [pin for pin in self.n5 + self.t5 if pin.available is True]
        target_pin = random.choice(available_outputs)
        self.call_match_and_remove_pin(target_pin, self.n5, self.t5)
        return target_pin

    def call_match_and_remove_pin(self, pin, pin_list1, pin_list2=None):
        super(Group5, self).match_and_remove_pin(pin, pin_list1, pin_list2)

class group6(pingroup):

    def __init__(self):
        #pingroup.__init__(self)
        super(pingroup, self).__init__()
        self.type = "standard"
        # list of available pins in group 6
        self.e6 = [pin("e6", i, self) for i in range(4)]
        self.i6 = [pin("i6", i, self) for i in range(3)]
        self.t6 = [pin("t6", i, self) for i in range(4)]
        self.n6 = [pin("n6", i, self) for i in range(4)]

    def get_input(self, pin_index):
        all_inputs = self.e6 + self.i6
        target_pin = all_inputs[pin_index]
        #self.match_and_remove(target_pin, self.e6, self.i6)
        self.call_match_and_remove_pin(target_pin, self.e6, self.i6)
        return target_pin

    def get_output(self, pin_index):
        all_outputs = self.n6 + self.t6
        target_pin = all_outputs[pin_index]
        #self.match_and_remove(target_pin, self.n6, self.t6)
        self.call_match_and_remove_pin(target_pin, self.n6, self.t6)
        return target_pin

    """
    returns a random available input
    """
    def get_random_input(self):
        available_inputs = [pin for pin in self.e6 + self.i6 if pin.available is true]
        target_pin = random.choice(available_inputs)
        self.call_match_and_remove_pin(target_pin, self.e6, self.i6)
        return target_pin

    """
    returns a random available input
    """
    def get_random_output(self):
        available_outputs = [pin for pin in self.n6 + self.t6 if pin.available is true]
        target_pin = random.choice(available_outputs)
        self.call_match_and_remove_pin(target_pin, self.n6, self.t6)
        return target_pin

    def call_match_and_remove_pin(self, pin, pin_list1, pin_list2=none):
        super(group6, self).match_and_remove_pin(pin, pin_list1, pin_list2)


class GroupPl(MotorSensorPinGroup):
    def __init__(self):
        #MotorSensorPinGroup.__init__(self)
        super(MotorSensorPinGroup, self).__init__()
        self.pins = [Pin("pl", i, self) for i in range(6)]


class GroupRl(MotorSensorPinGroup):
    def __init__(self):
        #MotorSensorPinGroup.__init__(self)
        super(MotorSensorPinGroup, self).__init__()
        self.pins = [Pin("rl", i, self) for i in range(6)]


class GroupRr(MotorSensorPinGroup):
    def __init__(self):
        #MotorSensorPinGroup.__init__(self)
        super(MotorSensorPinGroup, self).__init__()
        self.pins = [Pin("rr", i, self) for i in range(6)]


class GroupPr(MotorSensorPinGroup):
    def __init__(self):
        #MotorSensorPinGroup.__init__(self)
        super(MotorSensorPinGroup, self).__init__()
        self.pins = [Pin("pr", i, self) for i in range(6)]


class GroupBl(MotorSensorPinGroup):
    def __init__(self):
        #MotorSensorPinGroup.__init__(self)
        super(MotorSensorPinGroup, self).__init__()
        self.pins = [Pin("bl", i, self) for i in range(4)]


class GroupBr(MotorSensorPinGroup):
    def __init__(self):
        #MotorSensorPinGroup.__init__(self)
        super(MotorSensorPinGroup, self).__init__()
        self.pins = [Pin("br", i, self) for i in range(4)]


class GroupFl(MotorSensorPinGroup):
    def __init__(self):
        #MotorSensorPinGroup.__init__(self)
        super(MotorSensorPinGroup, self).__init__()
        self.pins = [Pin("fl", i, self) for i in range(4)]


class GroupFr(MotorSensorPinGroup):
    def __init__(self):
        #MotorSensorPinGroup.__init__(self)
        super(MotorSensorPinGroup, self).__init__()
        self.pins = [Pin("fr", i, self) for i in range(4)]
