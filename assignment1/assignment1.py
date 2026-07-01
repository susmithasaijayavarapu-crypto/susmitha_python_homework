#Task1
def hello():
    return "Hello!"

#Task2

def greet(name):
    return f"Hello, {name}!"

#Task3

def calc (a,b,c = "multiply"):
    if(c == "add"):
        return (a+b) 
    elif(c == "subtract"):
        return a-b
    elif(c == "divide"):
        try:
            return a/b
        except ZeroDivisionError as e:
            return "You can't divide by 0!"
    elif(c == "multiply"):
        try:
            return a*b
        except:
            return "You can't multiply those values!"
    elif( c == "modulo"):
        return a%b
    else :
        return a*b

#Task4

def data_type_conversion(value , data_type):
    try :
        if data_type == 'float':
            return float(value)
        elif data_type == 'int':
            return int(value)
        elif data_type == 'str':
            return str(value)
        else :
            return f"Unsupported data type: {data_type}"
    except (ValueError , TypeError):
        return f"You can't convert {value} into a {data_type}."
    
#Task5

def grade (*args):
    try :
        avg =  sum(args)/len(args)
    except:
        return "Invalid data was provided." 
    else :
        if avg >= 90 :
            return "A"
        elif (avg>=80 and avg <=89):
            return "B"
        elif (avg>=70 and avg <=79):
            return "C"
        elif(avg>=60 and avg <=69):
            return "D"
        elif(avg< 60) :
            return "F"
 #Task6
        
def repeat (str, count):
    result =""
    for i in range(count):
        result += str;
    return result

#Task7

def student_scores(mode,**scores):
    if (mode == "mean"):
        return sum(scores.values())/len(scores)
    elif(mode == "best"):
        return max(scores , key = scores.get)

  #Task8
    
def titleize(title):
     
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    words = title.split()
    if not words:
        return ""
    
    result = []
    
    for index, word in enumerate(words):
        
        if index == 0 or index == len(words) - 1 or word.lower() not in little_words:
            result.append(word.capitalize())
        else:
            
            result.append(word.lower())
            
    return " ".join(result)

#Task9

def hangman(secret,guess):
    result =[]
    for char in secret:
        if char in guess:
            result.append(char)
        else:
            result.append("_")
    return "".join(result)

#Task10

def pig_latin(sentence):
   
    vowels = "aeiou"
    words = sentence.split()
    result = []
    
    for word in words:
        if word[0] in vowels:
            # Starts with a vowel
            pig_word = word + "ay"
        else:
            # Consonant(s) move
            consonant_cluster = ""
            for i, char in enumerate(word):
                # Check for special 'qu' case
                if i > 0 and char == 'u' and word[i-1] == 'q':
                    consonant_cluster += char
                    break
                # Keep adding to cluster if it's a consonant
                elif char not in vowels:
                    consonant_cluster += char
                else:
                    # Found the first vowel
                    break
            
            # Move cluster to the end + ay
            pig_word = word[len(consonant_cluster):] + consonant_cluster + "ay"
            
        result.append(pig_word)
        
    return " ".join(result) 


        
        

        

