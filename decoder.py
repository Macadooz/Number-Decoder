###################################################################################################
#  TITLE: decoder.py																			  #
#																								  #
#  DESCRIPTION: Given an encoded message of integers such that a = 1, b = 2...                    #
#               return all possible decoded messages that integer could be.                       #
#               For example, 111 could be ak(1,11) ka(11,1) or aaa(111). 						  #
#               This is done by constructing a tree starting with Node 'S' 						  #
#               with every child Node either being the next ones place number 					  #
#               in the message or the next 10s place number. All of the   						  #
#               different paths of said tree contain all the different decoded					  #        
#               messages. 																		  #
#               Example tree for 111:															  #
#                                    S															  #
#                                  /   \														  #
#                                 1     11  													  #
#                                / \    														  #
#                               1  11  1														  #
#                              /																  #
#                             1																	  #
#              The program then generates all the possible paths down this tree by 				  #
#              generating a list of  all the possible binary numbers that are the				  #
#			   length of the message. It then uses these binary numbers as maps down			  #
#              the tree with a 0 meaning a left turn and a 1 meaning a right turn.				  #
#              Finally the program swaps all of the numbers with letters to get a 		 		  #
#              list of all the decoded messages and deletes any duplicates in the list			  #
#																								  #
#																								  #
#  AUTHOR: Mac Wolf			   																	  #
###################################################################################################

class Node():

	def __init__(self, name, msg):
		self.name = name
		self.children = []
		self.msg = msg
	
	def add_child(self, child):
		self.children.append(child)

	def create_tree(self):
		# This conditional breaks out of the function if it has already gone through the entire message 
		
		if self.msg == []:
			return
		
		place1 = self.msg[0]

		#try catch is for when the index goes out of range
		try:
			place10 = self.msg[0] + self.msg[1]
			# Any number above 26 can't represent a number in the Alphabet
			if int(place10) > 26:
				place10 = None
		except:
			place10 = None


		self.add_child(Node(place1, self.msg[1:]))
		self.add_child(Node(place10, self.msg[2:]))

		#checks if it has at least 1 child and then if it does sets that to the left turn
		if len(self.children) > 0:
		
			self.left = self.children[0]
		
		else:
		
			self.left = None
	
		#checks if it has at least 2 children and then if it does sets the second one to the right turn
		if len(self.children) > 1:
			
			self.right = self.children[1]
	
		else:
			
			self.right = None
		
		#recursively creates subtrees for the children
		for child in self.children:

			child.create_tree()

	#Generates all of the binary numbers of the same length as the message
	def generate_paths(self, answer = None, counter = 2):

		if answer == None:

			answer = ['1','0']
		# doubles the size of answer and adds 1 to the first half and 0 to the second half
		# because .append was giving me a lot of bugs I decided to just add on to the single dimensional list and make a multi dimensional list late
		answer += answer 

		for x in range(len(answer)/2):

			answer[x] += '1'
		
		for x in range(len(answer)/2, len(answer)):
		
			answer[x] +='0'
		
		if counter < len(self.msg):
		
			return self.generate_paths(answer, counter + 1)
		
		else:			
			#generates the multi dimensional list
			
			realAnswer = []			
			a = []			
			for i in range(len(answer)):

				for z in answer[i]:
					realAnswer.append(z)
				
				a.append(realAnswer)				
				realAnswer = []
		
			return a

	def duplicates(self, listt):
		answer = []

		for x in listt:
			# checks for duplicates and None becuase if a None is in a list the path is incomplete
			if x not in answer and None not in x:
				answer.append(x)
		
		return answer

	def traverse_tree(self):	
		paths = self.generate_paths()

		#goes through all the paths generated
		for x in range(len(paths)):
			current_path = start

			#following the path
			for y in range(len(paths[x])):				

				# try catch is because it breaks at the very beginning of the loop when y = 0
				try:
					#checks if it's hit a dead end marked by None or if it has already gone through the entire message
					if current_path.name == None or reduce(lambda a, b: a+b, paths[x][:y]) == reduce(lambda a, b: a+b, self.msg):
						
						paths[x]= paths[x][:y]
						break
				
				except:
					pass

				if paths[x][y] == '0' and hasattr(current_path, 'left'):

					paths[x][y] = current_path.left.name
					current_path = current_path.left

				elif paths[x][y] == '1' and hasattr(current_path, 'right'):

					paths[x][y] = current_path.right.name
					current_path = current_path.right

		return self.duplicates(paths)

	def decoder(self):
		#swaps numbers with the appropriate letters
		chars = 'abcdefghijklmnopqrstuvwxyz'
		results = self.traverse_tree()
		for x in range(len(results)):

			for y in range(len(results[x])):
				results[x][y] = chars[int(results[x][y]) - 1]

			results[x] = reduce(lambda a,b: a+b, results[x])

		return results


msg = raw_input("Enter number to be decoded\t")

start = Node('S', list(msg))

print int(msg)

start.create_tree()

print start.decoder()

