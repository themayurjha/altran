import sys


'''
This file accepts only one string input 
'''

'''
convert incoming string to json
'''


def convert_to_json(t, response, operation,flag):
	if len(t) > 3:
		if flag:
			response[operation] = []
			response = response[operation]
			flag = False
		else:
			response.append(dict())
			response[-1][operation] = []
			response = response[-1][operation]
	else:
		response.append({operation: {}})
		response = response[-1][operation]
	return response, flag


'''
Making Use of dynamic programming by splitting the string 
and then sending to to get converted to json format.
'''


def split_string(str_to_format, response, tmp, flag):
	tmp = response
	while True:
		if str_to_format[0] == '(' and str_to_format[1] == '(':
			str_to_format = str_to_format[1:-1]
		else:
			break
	t = str_to_format.split()
	mid = len(t) // 2
	if mid == 0:
		if '(' in t[0]:
			response[t[0][1]] = t[0][3]
		else:
			response[t[0][0]] = t[0][2]
		return

	elif t[mid] == "||":
		response, flag = convert_to_json(t,response,"or", flag)
	else:
		response, flag = convert_to_json(t, response, "and", flag)

	split_string(" ".join(t[:mid]), response, tmp, flag)
	split_string(" ".join(t[mid+1:]), response,tmp,flag)
	return tmp


'''
query_string_validation takes one parameter as string
and validates if the string is formatted correctly. If
it is, then this function calls create_json function
or else it exits the program.
'''

def query_string_validation(str_to_validate):
	stack = []
	flag = True
	for char in  str_to_validate:
		if char == '(' or char == ')':
			if len(stack) == 0 and char == ')':
				flag = False
			else:
				if char == '(':
					stack.append(char)
				else:
					if len(stack) > 0:
						stack.pop()
						continue
					else:
						flag = False
		else:
			continue
	if len(stack) > 0:
		flag = False

	if flag:
		formatted = split_string(str_to_validate.strip(), {}, {}, True)
		response = {"query":formatted}
		print(response)


	else:
		print("Invalid String")
		sys.exit()


'''
checks and validates if an input string is provided 
to the script
'''
if len(sys.argv) == 1:
	print("Please provide input string")
	sys.exit()
else:
	if len(sys.argv) > 2:
		print("Provide One input at a time")
		sys.exit()
	else:
		query_string_validation(sys.argv[1])
