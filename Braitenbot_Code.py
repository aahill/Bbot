
class pin:
    # group_id represents the group the pin belongs to
    # number identifies the pin number within the group
    def __init__(self, group_id, number, group):
        self.group_id = group_id
        self.number = number
        #self.group = group
        self.available = true
