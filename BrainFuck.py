import sys

# In case you done goof
class CompileExcpetion(Exception):
	pass
class RuntimeException(Exception):
	pass

def BrainFuck(code):
	# strip all of the non executable characters
	code = ''.join(c for c in code if c in '<>,.+-[]')

	# make sure while loops are correct
	braceCount = 0
	loop_stack = [] # queue for while loop jump 'pointers'
	loop_lookup = {} # dictionary to store the while loop jumps
	for x in range(len(code)):
		if code[x] == '[':
			braceCount += 1
			loop_stack.append(x)
		elif code[x] == ']':
			braceCount -= 1
			# all looping pointers are stored in this dictionary.
			# since python dictionaries are O(1), this is the easiest opition
			start = loop_stack.pop() 
			loop_lookup[x] = start - 1
			loop_lookup[start] = x
		if braceCount < 0:
			raise CompileExcpetion("ERROR: Miss matched braces.")
	if braceCount != 0:
		raise CompileExcpetion("ERROR: Expected another ] somewhere.")

	# Alright, lets start the actual program
	memory = [0]*30000 # as defined by Urban Meuller, the dude who made BrainFuck
	mem_ptr = 0 # points to current block of memory
	code_ptr = 0 # points to current executable byte

	while(code_ptr != len(code)):
		# increment block
		if code[code_ptr] == '+':
			memory[mem_ptr] += 1
			if memory[mem_ptr] >= 256:
				raise RuntimeException("Integer Overflow")
		# decrement block
		elif code[code_ptr] == '-':
			memory[mem_ptr] -= 1
			if memory[mem_ptr] < 0:
				raise RuntimeException("Integer Underflow")
		# move pointer one block to the right
		elif code[code_ptr] == '>':
			mem_ptr += 1
			if mem_ptr > 30000:
				raise RuntimeException("Over memory bounds")
		# move pointer one block to the left
		elif code[code_ptr] == '<':
			mem_ptr -= 1
			if mem_ptr < 0:
				raise RuntimeException("Under memory bounds")
		# write character 
		elif code[code_ptr] == '.':
			sys.stdout.write(chr(memory[mem_ptr]))
		# read character
		elif code[code_ptr] == ',':
			memory[mem_ptr] = ord(sys.stdin.read(1))
		# loop start
		elif code[code_ptr] == '[':
			if memory[mem_ptr] == 0:
				code_ptr = loop_lookup[code_ptr]
		# loop ending
		elif code[code_ptr] == ']':
			code_ptr = loop_lookup[code_ptr]
		code_ptr += 1

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: python BrainFuck.py <brain_fuck_source>"
		exit()
	try:
		f = open(sys.argv[1])
	except IOError:
		print "Error reading file: " + sys.argv[1]
		exit()
	code = f.read()
	BrainFuck(code)