import traceback

def main():
    try:
        # Open diary.txt in append mode
        with open("diary.txt", "a") as diary_file:
            first_run = True
            
            while True:
                # Determine the prompt text
                if first_run:
                    prompt = "What happened today? "
                    first_run = False
                else:
                    prompt = "What else? "
                
                # Get input from the user
                user_input = input(prompt)
                
                # Write the input to the file
                diary_file.write(user_input + "\n")
                
                # Check for the exit condition
                if user_input.lower() == "done for now":
                    break

    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
    
if __name__ == "__main__":
    main()