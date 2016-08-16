import random
from BaseAndInstructionSet import *

class Decoder(object):
    def __init__(self):
        self.index = 0

    
    
    def decode_binary(self, binary_list):
        # turn binary list into a string for easy comparison
        binary_string = ""
        for binary_digit in binary_list:
            binary_string += str(binary_digit)
    
        # determines what number each 4bit binary string represents
        if binary_string == "0000":
            return 0
        elif binary_string == "0001":
            return 1
        elif binary_string == "0010":
            return 2
        elif binary_string == "0011":
            return 3
        elif binary_string == "0100":
            return 4
        elif binary_string == "0101":
            return 5
        elif binary_string == "0110":
            return 6
        elif binary_string == "0111":
            return 7
        elif binary_string == "1000":
            return 8
        elif binary_string == "1001":
            return 9
        elif binary_string == "1010":
            return 10
        elif binary_string == "1011":
            return 
        elif binary_string == "1100":
            return  
        elif binary_string == "1101":
            return  
        elif binary_string == "1110":
            return  
        elif binary_string == "1111":
            return  

    def binary_to_decimal(self, binary_list):
        dec_list = []
        # step through the array in 4s as long as there are enough digits (4) to form a number.
        # this is checked through the expression (len - 4) - (5 % 4)
        #print
        for x in range(0, len(binary_list)-3, 4):
            # generate the list of binary to be decoded
            temp = [binary_list[y] for y in range(x, x+4)]
            dec_list.append(self.decode_binary(temp))
        #    print temp, dec_list 
        #print
        #print 'Hypothetical # of decimal digits: %s/4 = %s. Actual #: %s'% (len(binary_list), len(binary_list)/4, len(dec_list))
        #print
        return dec_list
        #print
    

    def generate_coords(self, binaryList):
        """
        method for getting the next non-NONE value from decList
        return: either the value of decList at index self.index, unless an error is found; in which case
        return -1
        """
        coords = []
        #this value is the height of the matrix created by the pin-group
        #HEIGHT_OF_PINGROUP = 21  -- Not sure why 21 was chosen
        HEIGHT_OF_PINGROUP = 30
        #print binaryList
    
        def get_next_val():
            """
            gets the next value from decList, which is the list containing the decimal translation of the binary string
            If this causes an index error, -1 will be returned to avoid the error from halting the program
            :return: the next value form decList. Here None values can be taken to represent intronic regions of the gene
            in question.
            """
            #print decList
            to_return = None
            try:
                while to_return is None:
                    to_return = decList[self.index]
                    self.index += 1
            except IndexError:
                self.index = -1
                return -1
            #print "index: %s  Next decimal digit: %s" % (self.index, to_return) 
            return to_return
            #print
        
        
        # the input decList must have at least one digit for the creation of the initial pin coordinate,
        # and 3 more for the creation of a terminal pin.
        # If this condition is met, generate initial x,y coord from first value in the array
        decList = self.binary_to_decimal(binaryList)
        #print "Direction key: 0: y+=Distance,1:x+=distance, y+=distance, 2:x+=distance, 3:x=distance, y-=distance\n"+\
        #"4:y-=distance, 5:x-=distance, y-=distance, 6: x-=distance, 7: x-=distance, y-=distance"
        #print decList
        if len(decList) < 3:
            return []
        else:
            x = get_next_val()
            # the inital pin coordinate will range from zero to the length of the matrix created by the pin group
            #y = random.randint(0,HEIGHT_OF_PINGROUP)
            y = get_next_val() #Jake addition: no reason we need to selcet randomly. We 
                                # generate perfectly good nonrandom numbers
            #print 'Original (x,y): (%s,%s)' % (x,y)
        
            # append first xy coordinate in the form of a 2-tuple
           # z = get_next_val() # jake addition: this decides which pin will be the origin
                                # of the subsequent connection
            coords.append((x,y))
        
            # do the following for every digit after the first (since it was used to generate
            # a starting position)
            # also check for the minimum required digits for the thread instruction process
            while self.index < len(decList):# and (len(decList) - self.index) >= 4:
                # generate the x coordinate's direction, and end pin
                # this number will be 1 through 8, corresponding to the different
                # cardinal directions
                pos1 = get_next_val()
                pos2 = get_next_val()
                pos3 = get_next_val()
                """ try:
                    pos4 = get_next_val() #Jake addition: this decides the origin
                except(IndexError):
                    pass"""
                # the pos1 and pos2 values are used for direction and cannot be negative. Similarly, pos3 is used for
                # distance, and must be greater than 0
                if pos1 < 0 or pos2 < 0 or pos3 <= 0:
                    #print 'Break! a decimal <= 0 was generated'
                    #print 'possible culprits: pos1:%s,pos2:%s,pos3:%s' % (pos1,pos2,pos3)
                    break
        
                direction = (pos1 + pos2) % 8
                distance = pos3
                if direction == 0:
                    y += distance
                elif direction == 1:
                    y += distance
                    x += distance
                elif direction == 2:
                    x += distance
                elif direction == 3:
                    x += distance
                    y -= distance
                elif direction == 4:
                    y -= distance
                elif direction == 5:
                    y -= distance
                    x -= distance
                elif direction == 6:
                    x -= distance
                elif direction == 7:
                    y += distance
                    x -= distance
                if x < 0 or y < 0:
                    #print 'Break! x or y < 0'
                    #print '(%s,%s)' % (x,y)
                    break
                #print'Direction: (next_val + next_val ) mod 8 --> (%s + %s) mod 8 = %s' % (pos1, pos2, direction)
                #print 'Distance: next_val ---> %s' % distance
                #print 'Direction: %s, Distance: %s --->(%s,%s)' % (direction, distance ,x,y)
               # if self.index in [5 +i*3 for i in range(len(decList))]:
               #Jake addition: adds third coordiante, z :which determines origin
               #of the subsequent wire connection in a thread.
                z = get_next_val()
                if z < 0:
                    #print 'Break! z < 0'
                    #print'z = %s' % z
                    break
                else:
                     coords.append((x,y,z))
                     x = z # This sets x to be the origin of the subsequent wire connection (z).
                #print
                #print 'Coord z: %s. Final coords: (%s,%s,%s)' % (z,x,y,z)
               # else:
                #    coords.append((x, y))
        
        #print 'Resultant Coords:', coords
        self.index = 0
        return coords
