import pymysql as mc 

connection = mc.connect(host="localhost",user="root",password="1234",database="CSProject")
cursor = connection.cursor()

def view_books():
    cursor.execute("select * from Books")
    rows = cursor.fetchall()
    if rows:
        print("\n===== |BOOKS TABLE| =====\n")
        for row in rows:
            print(row)
    else:
        print("No books found...")
        
        
def view_loans():
    cursor.execute("select * from BookLoan")
    rows = cursor.fetchall()
    if rows:
        print("\n===== |LOANS TABLE| =====\n")
        for row in rows:
            print(row)
    else:
        print("No loans found...")


def add_loan():
    loan_id = input("Enter Loan ID: ")
    book_id = input("Enter Book ID: ")
    member_id = input("Enter Member ID: ")
    loan_date = input("Enter Loan Date (YYYY-MM-DD): ")
    return_date = input("Enter Due Date (YYYY-MM-DD): ")
    cursor.execute("select TotalCopies from Books where BookID = %s", (book_id,))
    copies = cursor.fetchone()
    if not copies:
        print("Book ID not found.")
        return
    count = copies[0]
    if count <= 0:
        print("Book unavailable...")
        return 
    cursor.execute("insert into BookLoan values(%s, %s, %s, %s, %s)", (loan_id, book_id, member_id, loan_date, return_date))
    cursor.execute("update Books set TotalCopies = TotalCopies - 1 where BookID = %s", (book_id,))
    connection.commit()
    print("Loan added successfully...")


def return_loan():
    loan_id = input("Enter Loan ID: ")
    cursor.execute("select LoanID from BookLoan where LoanID = %s", (loan_id,))
    loan = cursor.fetchone()
    if not loan:
        print("Loan ID is invalid..")
        return    
    cursor.execute("select BookID from BookLoan where LoanID = %s", (loan_id,))
    book = cursor.fetchone()
    if book:
        cursor.execute("update Books set TotalCopies = TotalCopies + 1 where BookID = %s", (book[0],))
        cursor.execute("delete from BookLoan where LoanID = %s", [loan_id])
        connection.commit()
        print("Thank you for returning the book..")
        print("Your loan has been repayed...")
        

def new_book():
    book_id = input("Enter the BookID: ")
    book_name = input("Enter the Book's Name: ")
    author = input("Enter the Author's Name: ")
    count = int(input("Enter the number of copies: "))
    cursor.execute("insert into Books values(%s, %s, %s, %s)", [book_id, book_name, author, count])
    connection.commit()
    print("Book successfully added in stock...")


def delete_book():
    book_id = input("Enter the BookID to be deleted: ")
    cursor.execute("delete from Books where BookID = (%s)", [book_id])
    connection.commit()
    print("Deletion Successful..")


while True:
    print("\n====== |LIBRARY MENU| ======\n")
    print("1. View Books Table")
    print("2. View Loans Table")
    print("3. Add a Loan")
    print("4. Return a Loan")
    print("5. Add a New Book")
    print("6. Delete a Book from Stock")
    print("7. Exit\n")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        view_books()
    elif choice == 2:
        view_loans()
    elif choice == 3:
        add_loan()
    elif choice == 4:
        return_loan()
    elif choice == 5:
        new_book()
    elif choice == 6:
        delete_book()
    elif choice == 7:
        print("Successfully Exitted...")
        break
    else:
        print("Please Try Again..")
    
    task = input("\nDo you wish to continue(y/n): ")
    if task.lower() == 'n':
        print("Successfully Exitted...")
        break


cursor.close()
connection.close()
