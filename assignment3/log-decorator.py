import logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))


def logger_decorator(func):
    def wrapper(*args, **kwargs):
       
        result = func(*args, **kwargs)
        pos_params = list(args) if args else "none"
        k_params = kwargs if kwargs else "none"
        log_message = (
            f' function: {func.__name__} \n'
            f"positional parameters: {pos_params}\n"
            f"keyword parameters: {k_params}\n"
            f"return: {result}"
            )
        logger.log(logging.INFO, log_message)

        return result
    return wrapper
@logger_decorator
def no_params():
    print ("Hello World")

@logger_decorator
def pos_params(*args):
    print (f"The length of positional parameters is {len(args)}")
    return True
@logger_decorator
def key_params(**kwargs):
    print(f"The given keyword parameters are :{kwargs}")
    return logger_decorator

if __name__ == "__main__":
    print ("running decorated functions")
    no_params()
    pos_params('apple',"banana",'grapes')
    key_params( name= "fruits", count=3, has_data= True)
    print("execution completed")