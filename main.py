from pagbank_crawler import run_pagbank_crawler
from yuno_crawler import run_yuno_scraper
from pagbank_get_all_text import run_pagbank_text_reader
from yuno_get_all_text import run_yuno_text_reader
from time import sleep


def password_check():
    password = input("Enter password: ")
    is_correct = password == "123456"
    tries = 3
    while not is_correct:
        sleep(0.5)
        password = input(f"Wrong password... Try again({tries}): ")
        is_correct = password == "123456"
        tries -= 1
        if tries == 0:
            break
    return is_correct


def invalid_choice():
    print("------------------------------------------")
    print("Invalid choice. Please enter 1, 2, or 3.")
    sleep(1)


def yuno_choices():
    while True:
        print("------------------------------------------")
        print("Do you want to:")
        print("------------------------------------------")
        print("1. Run bot")
        print("2. Update translated content")
        print("3. Go back")
        print("------------------------------------------")

        yuno_choice = input("Enter the number of your choice: ")
        sleep(0.5)

        if yuno_choice == "1":
            run_yuno_scraper()
        elif yuno_choice == "2":
            correct_password = password_check()
            if correct_password:
                run_yuno_text_reader()
            else:
                break
        elif yuno_choice == "3":
            break
        else:
            invalid_choice()


def pagbank_choices():
    while True:
        print("Do you want to:")
        print("1. Run bot")
        print("2. Update translated content")
        print("3. Go back")
        print("------------------------------------------")

        pagbank_choice = input("Enter the number of your choice: ")

        if pagbank_choice == "1":
            run_pagbank_crawler()
        elif pagbank_choice == "2":
            correct_password = password_check()
            if correct_password:
                run_pagbank_text_reader()
        elif pagbank_choice == "3":
            break
        else:
            invalid_choice()


def main():
    while True:
        print("------------------------------------------")
        print("Which service do you want to work with?")
        print("------------------------------------------")
        print("1. Yuno")
        print("2. Pagbank")
        print("3. Exit")
        print("------------------------------------------")

        service_choice = input("Enter the number of your choice: ")
        sleep(0.5)

        if service_choice == "1":
            yuno_choices()

        elif service_choice == "2":
            pagbank_choices()

        elif service_choice == "3":
            print("Exiting...")
            sleep(2)
            break
        else:
            invalid_choice()


if __name__ == "__main__":
    main()
