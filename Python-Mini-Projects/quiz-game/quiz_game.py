print("Welcome to my Computer quiz ")

playing = input("Do you want to play? ")

if playing.lower() != "yes":
  quit()


print("Okay! let us play :) ")
score = 0;

answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
  print('Correct!')
  score += 1

else: 
  print("Incorrecct!")

answer = input("What does GPU stand for? ")
if answer.lower() == "graphics processing unit":
  print('Correct!')
  score += 1

else: 
  print("Incorrecct!")

answer = input("What does RAM stand for? ")
if answer.lower() == "random access memory":
  print('Correct!')
  score += 1

else: 
  print("Incorrecct!")

answer = input("What does PSU stand for? ")
if answer.lower() == "power supply unit":
  print('Correct!')
  score += 1

else: 
  print("Incorrecct!")


print("\nYou got " + str(score) + " questions correct!")
print("\nYou got " + str((score/4) * 100) + "%. ")
