"""
Have a look at the script called 'human-guess-a-number.py' (in the same folder as this one).

Your task is to invert it: You should think of a number between 1 and 100, and the computer 
should be programmed to keep guessing at it until it finds the number you are thinking of.

At every step, add comments reflecting the logic of what the particular line of code is (supposed 
to be) doing. 
"""

# Define the search range: the computer knows the number is between 1 and 100
low = 1   # Lower bound of the range
high = 100  # Upper bound of the range

print("Think of a number between 1 and 100.")
print("I will try to guess it. Tell me if my guess is '<' (too big), '>' (too small), or '=' (correct).")

# Start the guessing loop
while True:
    # Computer makes a guess: pick the middle of the range
    guess = (low + high) // 2  
    print("My guess is:", guess)

    # Ask the user if the guess is correct, too big, or too small
    feedback = input("Is your number '<' (smaller), '>' (bigger), or '=' (correct)? ")

    # If guess was correct, break the loop
    if feedback == "=":
        print("Yay! I found your number:", guess)
        break

    # If the number is smaller, adjust the upper bound
    elif feedback == "<":
        high = guess - 1

    # If the number is bigger, adjust the lower bound
    elif feedback == ">":
        low = guess + 1

    # If invalid input, ask again without changing range
    else:
        print("Please enter '<', '>' or '=' only.")