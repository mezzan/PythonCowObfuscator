def print_options():
    print("Options:")
    print(" 'p' print options")
    print(" 'c' convert from celsius")
    print(" 'f' convert from fahrenheit")
    print(" 'q' quit the program")

def celsius_to_fahrenheit(c_temp):
    return 9.0/5.0*c_temp+32

def fahrenheit_to_celsius(f_temp):
    return (f_temp - 32.0)*5.0/9.0    