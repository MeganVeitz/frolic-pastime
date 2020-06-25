#Towers of Hanoi is an ancient mathematical puzzle that starts off with three stacks and many disks.The objective of the game is to move the stack of disks from the leftmost stack to the rightmost stack.

#The game follows three rules:
#Only one disk can be moved at a time.
#Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack or on an empty rod.
#No disk may be placed on top of a smaller disk.

from stack import Stack

print("\nLet's play Towers of Hanoi!!")

#Create the Stacks
stacks = []
left_stack = Stack("Left")
middle_stack = Stack("Middle")
right_stack = Stack("Right")
stacks += [left_stack, middle_stack, right_stack]

#Set up the Game
num_disks = int(input("\nHow many disks do you want to play with?\n"))

while num_disks < 3:
  num_disks = int(input("Enter a number greater than or equal to 3\n"))

for disk in range(num_disks, 0, -1):
  left_stack.push(disk)
#left_stack.print_item()

num_optimal_moves = (2** num_disks) -1
print("\nThe fastest you can solve this game is in {0} moves".format(num_optimal_moves))

#Get User Input
def get_input():
  #use stack.get_name to set choices to a list of names
  #accessing first letter of stacks name using [0]
  choices = [stack.get_name()[0] for stack in stacks]

  counter = 0 
  while True:
    counter += 1
    if counter > 5:
      print("counter more than 5")
      break 
    for i in range(len(stacks)):
      name = stacks[i].get_name()
      letter = choices[i]
      print("Enter {0} for {1}".format(letter, name))
    user_input = input("")

    if user_input in choices:
      for i in range(len(stacks)):
        return stacks[i]

        
#Play the Game
num_user_moves = 0 

while right_stack.get_size != num_disks:
  print("\n\n\n...Current Stacks...")
  for stack in stacks:
    stack.print_items()

  counter = 0 
  while True:
    counter += 1
    if counter > 5:
      print("counter more than 5")
      break 
    print("\nWhich stack do you want to move from?\n")
    from_stack = get_input()
    print("\nWhich stack do you want to move to?\n")
    to_stack = get_input()

    if from_stack.get_size() == 0:
      print("\n\nInvalid Move. Try Again")

    elif to_stack.get_size == 0 or from_stack.peek() < to_stack.peek():
      disk = from_stack.pop()
      to_stack.push(disk)
      num_moves += 1
      break
  else:
    print("\n\nInvalid Move. Try Again")
  


print("\n\nYou completed the game in {0} moves, and the optimal number of moves is {1}".format(num_user_moves, num_optimal_moves))
    
    
