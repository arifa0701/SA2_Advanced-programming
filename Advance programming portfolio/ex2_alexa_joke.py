"""Alexa joke"""
import random  # Importing the random module to select random jokes

def load_jokes(filename):
    """Load jokes from a file and split them into setup and punchline."""
    jokes = []  # List to store jokes
    try:
        with open(filename, 'r', encoding='utf-8') as file:  # Open the jokes file
            for line in file:
                line = line.strip()  # Remove extra spaces and newlines
                if '?' in line:  # Check if there is a question mark in the joke
                    setup, punchline = line.split('?', 1)  # Split setup and punchline
                    jokes.append((setup.strip() + '?', punchline.strip()))  # Add to list
    except FileNotFoundError:
        print("Error: randomJokes.txt file not found!")  # Error if file is missing
    return jokes  # Return list of jokes

def tell_joke(jokes):
    """Display a random joke: setup first, punchline after user input."""
    joke = random.choice(jokes)  # Pick a random joke
    print("\n" + joke[0])  # Print the setup
    input("Press Enter to hear the punchline...")  # Wait for user input
    print(joke[1] + "\n" + "=" * 40)  # Show the punchline and separator

def main():
    jokes = load_jokes("resources/randomJokes.txt")  # Load jokes from file
    if not jokes:
        print("No jokes loaded. Exiting program.")  # Exit if no jokes found
        return
    
    # Display welcome message and instructions
    print("=" * 30)  
    print("          JOKER ALEXA")
    print("=" * 30) 
    print("Type 'Alexa tell me a joke' to hear one")
    print("Type 'quit' or 'exit' to end the program")  
    print("=" * 30)  

    # Main loop to interact with user
    while True:
        user_input = input("\nHi,whats up? ").strip().lower()  # Take user input
        
        if user_input == "alexa tell me a joke":
            tell_joke(jokes)  # Tell a random joke
        elif user_input in ["quit", "exit"]:
            print("\nI hope you keep laughing like this haha.. Goodbye!")  # Exit message
            break  # Exit loop
        else:
            print('I didn\'t understand that. Try saying: "Alexa tell me a joke"')  # Invalid input

# Run the main function
if __name__ == "__main__":
    main()
