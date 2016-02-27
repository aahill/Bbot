from PinAndPinGroup import *

#emulates the sequence of pins in an organism
def get_pin(x,y,input_or_output):
	group1 = Group1()
	group2 = Group2()
	group3 = Group3()
	group4 = Group4()
	group5 = Group5()
	group6 = Group6()
	groupPl = GroupPl()
	groupRl = GroupRl()
	groupRr = GroupRr()
	groupPr = GroupPr()
	groupBl = GroupBl()
	groupBr = GroupBr()
	groupFl = GroupFl()
	groupFr = GroupFr()
	# organize pin groups into a single list
	pinGroups = [group1, group2, group3, group4, group5, group6, groupPl,
	                groupRl, groupRr, groupPr, groupBl, groupBr, groupFl, groupFr]

	try:
		if input_or_output == "input":
			pin = pinGroups[x].get_input(y)
		else:
			pin = pinGroups[x].get_output(y)
		print "Pin at ", x, " ", y, ": ", pin.group_id+str(pin.number)
	except IndexError:
		print "index error: no pin at : ",x, ", ",y, " for ", input_or_output



get_pin(6,3,'output')
get_pin(6,3,'input')