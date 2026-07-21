def make_hangman(secret_word):
    guesses=[]
    def hangman_closure(letter):
      
        if letter not in guesses:
            guesses.append(letter.lower())
            
        
        current_display = []
        all_guessed = True
        
        for char in secret_word.lower():
            if char in guesses:
                current_display.append(char)
            else:
                current_display.append("_")
                all_guessed = False
                
        
        print("Word progress:", "".join(current_display))
      
        return all_guessed
        
    return hangman_closure


if __name__ == "__main__":
    print("--- Welcome to Hangman ---")
    secret = input("Enter the secret word: ").strip()
    
    play_hangman = make_hangman(secret)
    
    print("\nGame started! Guess the word letter by letter.")
    
    won = False
    while not won:
        guess_letter = input("Enter a letter: ").strip()
        
        if len(guess_letter) != 1:
            print("Please enter a single letter.")
            continue
            
        won = play_hangman(guess_letter)
        
        if won:
            print("\nCongratulations! You've guessed the whole word!")
