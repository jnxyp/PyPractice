
def ask_question(prompt):
	user_input = input(prompt)
	while user_input.upper() not in ['YES', 'NO']:
		print("- Please answer using either yes or no. ", end = '')
		user_input = input()
	return user_input
	
def make_a_guess(object):
	print(object)
	_ = input("- Was this the correct answer?")
	exit()