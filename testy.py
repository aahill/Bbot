# Need these to test match_and_remove_pins
class Pin:
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
    
 
 
pin1 = pin(2,1,1)
pin2 = pin(1,3,4)
piny = pin(1,1,1) #piny is identical to pin1, thus pin1 should be made unavailable
pingroup= PinGroup()

list1 = [pin2, pin1]
print "pin1 avaialability before match_and_remove is called:", pin1.available 
pingroup.match_and_remove_pin(piny, list1)
print "Pin1 availability after:", pin1.available
