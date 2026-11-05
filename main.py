menu = ["pizza", "burger", "salad", "pasta", "sushi"]




def main():
    print("welcome to the restaurant!")

    user_input = input("please enter your command:")

    if user_input == "menu":
        print("heres the menu:")
        for item in menu:
            print(item)

main()