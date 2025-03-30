import re

def start():
    while ValueError:
        print("Welcome to PDF Search Engine!")
        print("There are several commands at your disposal:")
        print("1. Search")
        print("2. Guide")
        print("0. Exit")
        try:
            choice = input("Enter your choice: ")
            match choice:
                case "1":
                    query = input("Enter query: ")
                    return query.lower()
                case "2":
                    print("Search Options Guide \n\n")
                    print("  For single word search just insert desired query eg. python")
                    print("  For multiple word search insert words with space in between them eg. linked list node")
                    print("  Put your query in \" if you want to search whole phrase eg. \" linked list node \" ")
                    print("  In order to create complex logical queries use parentheses () and AND/OR/NOT operators eg. (python AND node) OR list ")
                    print("  For autocomplete insert query + * at the end eg. fun* -> function, functionality \n\n")
                    choice = input("Enter something to return: ")
                case "0":
                    exit()
                case _:
                    print("Invalid choice")
        except ValueError:
            print("Invalid choice")