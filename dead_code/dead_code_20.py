while ppppppp != "q":
    if ppppppp == "c":
        temp = input("Celsius temperature:")
        print("Fahrenheit:",celsius_to_fahrenheit(temp))
    elif ppppppp == "f":
        temp = input("Fahrenheit temperature:")
        print("Celsius:",fahrenheit_to_celsius(temp))
    elif ppppppp == "q":
        print_options()
    else:
        ppppppp = "OMG!! It's cow language <3 !!"

    break