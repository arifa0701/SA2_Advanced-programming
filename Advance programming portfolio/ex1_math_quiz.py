"""Math Quiz"""
import random
def displayMenu():
    """Display the difficulty level menu"""
    print("\n" + "="*40)
    print("         MATHS QUIZ")
    print("="*40)
    print("DIFFICULTY LEVEL")
    print(" 0. Back to Main Menu")
    print(" 1. Easy (1-digit numbers)")
    print(" 2. Moderate (2-digit numbers)")
    print(" 3. Advanced (4-digit numbers)")
    
    print("="*40)

def randomInt(difficulty):
    """Generate random numbers based on difficulty level"""
    if difficulty == 1:  # Easy - 1 digit
        return random.randint(0, 9)
    elif difficulty == 2:  # Moderate - 2 digits
        return random.randint(10, 99)
    else:  # Advanced - 4 digits
        return random.randint(1000, 9999)

def decideOperation():
    """Randomly decide between addition or subtraction"""
    return '+' if random.randint(0, 1) == 0 else '-'

def displayProblem(num1, num2, operation):
    """Display the problem and get user's answer"""
    print(f"\n{num1} {operation} {num2} = ", end="")
    try:
        answer = int(input())
        return answer
    except ValueError:
        print("Please enter a valid number!")
        return displayProblem(num1, num2, operation)

def isCorrect(num1, num2, operation, user_answer):
    """Check if the user's answer is correct and provide feedback"""
    if operation == '+':
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2
    
    if user_answer == correct_answer:
        print("Correct!")
        return True
    else:
        print(f"Incorrect. Try again to get +5 points")
        return False

def displayResults(score):
    """Display final results and grade"""
    print("\n" + "="*40)
    print("           QUIZ RESULTS")
    print("="*40)
    print(f"Your score: {score}/100")
    
    # Determining ratings and commenting on the user performance
    if score >= 90:
        rate = "5 star"
        comment = "Excellent work!"
    elif score >= 80:
        rate = "4 star"
        comment = "Great job!"
    elif score >= 70:
        rate = "3 star"
        comment = "Good effort!"
    elif score >= 60:
        rate = "2 star"
        comment = "Not bad!"
    elif score >= 50:
        rate = "1 star"
        comment = "You passed!"
    else:
        rate = "0 star"
        comment = "Keep practicing!"
    
    print(f"Ratings: {rate}")
    print(f"{comment}")
    print("="*40)

def getDifficultyChoice():
    """Get difficulty level from user with option to go back"""
    while True:
        try:
            choice = int(input("Select difficulty (1-3) or 0 to go back: "))
            if choice == 0:
                return None  # Signal to go back to main menu
            elif 1 <= choice <= 3:
                return choice
            else:
                print("Please enter 0, 1, 2, or 3")
        except ValueError:
             print("Please enter a valid number!") #if user choosed a wrong digit or invalid number

def playQuiz():
    """Main function to play one round of the quiz"""
    # Display menu and get difficulty level
    displayMenu()
    
    difficulty = getDifficultyChoice()
    if difficulty is None:  # User chose to go back
        return None
    
    score = 0
    total_questions = 10
    
    print(f"\nStarting quiz with {total_questions} questions...")
    
    for question_num in range(1, total_questions + 1):    #ranging the questions from 1-10 using +1 function
        print(f"\nQuestion {question_num}/{total_questions}")
        
        # Generating numbers and operation
        num1 = randomInt(difficulty)
        num2 = randomInt(difficulty)
        operation = decideOperation()
        
        # Ensure subtraction doesn't give negative results for better user experience
        if operation == '-' and num1 < num2:
            num1, num2 = num2, num1
        
        # First attempt
        user_answer = displayProblem(num1, num2, operation)
        
        if isCorrect(num1, num2, operation, user_answer):
            score += 10
            print("+10 points!")
        else:
            # Second attempt
            print("Second attempt:")
            user_answer = displayProblem(num1, num2, operation)
            
            if isCorrect(num1, num2, operation, user_answer):
                score += 5
                print("+5 points!")
            else:
                print("0 points for this question.")

# Display final results
    displayResults(score)
    return score
    
def main():
    """Main program loop"""

    print("Welcome to the Maths Quiz!")
    while True:
        total_score = playQuiz()
        
        # Ask if user wants to play again
        play_again = input("\nWould you like to play again? (y/n): ").lower()
        if play_again not in ['y', 'yes']:
            print("\nThanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()