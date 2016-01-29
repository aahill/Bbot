from ..Decoder.py import *

from nose.tools import *


#list of all 4bit binary words
#NOTE: we are only allowing wires to bridge pins at lenghts of up to 10;
#Therefor, the decoder will only translate the corresponding binary representations
binary_words =[
"0000", #0
"0001", #1
"0010", #2
"0011", #3
"0100", #4
"0101", #5
"0110", #6
"0111", #7
"1000", #8
"1001", #9
"1010", #10
]

def reset_decoder():
	test_decoder = Decoder

 
test_decoder = Decoder()

"""
test decoding of 4bit binary by ensuring a binary string containing all permutations of 
4 binary 'words' get translated correctly
i.e. 0000,0001,0010...1111 gets translated to 0,1,2,...,15
"""
def test_binary_decoding():
	for x in range(len(binary_words)):
		to_decode = test_decoder.decode_binary(binary_words[x])
		assert_equal(x, to_decode), "binary not translated correctly"

"""
test the decoding of a list of binary digits to decimal
"""
def test_binary_list_to_decimal():
	#create a list of 'bits' (1s and 0s) from the list of binary words
	list_of_binary = []
	for binary_word in binary_words:
		for bit in binary_word:
			list_of_binary.append(bit)
	#binary to decimal translations from the decoder
	list_of_dec = test_decoder.binary_to_decimal(list_of_binary)
	#check if the individual values of the list are as expected
	for x in range(len(list_of_dec)):
		assert_equal(x, list_of_dec[x])

"""
test the translation of a binary list containing multiple digits
"""
def test_multi_digit_binary_list():
	#below string translates to the decimal '1' repeated 8 times
	test_input = "00010001000100010001000100010001"
	output = test_decoder.binary_to_decimal(test_input)
	expected_output = [1 for x in range(8)]
	assert_equal(expected_output, output)


def test_generate_coords():
	#below string translates to the decimal '1' repeated 8 times
	test_input = "00010001000100010001000100010001"
	test_output = test_decoder.generate_coords(test_input)
	print test_output
	assert_equal(test_output, [(1,1),(2,1,1)])

"""
ensure the decoder outputs and empty list of coordinates when
given an empty binary string
"""
def test_generate_coords_on_empty_input():
	#test the method on an empty string, which should return an empty list
	empty_test_input = ""
	test_output2 = test_decoder.generate_coords(empty_test_input)
	assert_equal(test_output2, [])

