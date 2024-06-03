from pagbank_crawler import run_pagbank_crawler
from yuno_crawler import run_yuno_scraper
from pagbank_get_all_text import run_pagbank_text_reader
from yuno_get_all_text import run_yuno_text_reader


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

        if service_choice == "1":
            while True:
                print("------------------------------------------")
                print("Do you want to:")
                print("------------------------------------------")
                print("1. Run crawler")
                print("2. Update translated content")
                print("3. Go back")
                print("------------------------------------------")

                yuno_choice = input("Enter the number of your choice: ")

                if yuno_choice == "1":
                    run_yuno_scraper()
                elif yuno_choice == "2":
                    run_yuno_text_reader()
                elif yuno_choice == "3":
                    break
                else:
                    print("------------------------------------------")
                    print("Invalid choice. Please enter 1, 2, or 3.")
        elif service_choice == "2":
            while True:
                print("Do you want to:")
                print("1. Run crawler")
                print("2. Update translated content")
                print("3. Go back")
                print("------------------------------------------")

                pagbank_choice = input("Enter the number of your choice: ")

                if pagbank_choice == "1":
                    run_pagbank_crawler()
                elif pagbank_choice == "2":
                    run_pagbank_text_reader()
                elif pagbank_choice == "3":
                    break
                else:
                    print("------------------------------------------")
                    print("Invalid choice. Please enter 1, 2, or 3.")
                    print("------------------------------------------")
        elif service_choice == "3":
            print("Exiting...")
            break
        else:
            print("------------------------------------------")
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
