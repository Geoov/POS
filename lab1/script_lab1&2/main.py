import sys

import mysql.connector
import pymongo

mydb = mysql.connector.connect(user='root', password='mysqlroot',
                               host='127.0.0.1',
                               database='biblioteca')


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb_mongo = myclient["biblioteca"]

users_coll = mydb_mongo["users"]
messages_coll = mydb_mongo["messages"]

# mycursor = mydb.cursor()
#
# sql_insert_manager = 'INSERT INTO users(role_id, first_name, last_name, password, email, telephone) VALUES(%i, %s,
# %s, %s, %s, %s)' values_manager = ('0', 'George', 'Vrinceanu', 'test_pss', 'george_vrinceanu@staff.tuiasi.ro',
# '0771221015') mycursor.execute(sql_insert_manager, values_manager)

# mydb.commit()

# print(mycursor.rowcount, 'record inserted.')

# mydb.close()

global role
role = ''

global id_manager
id_manager = ''

global id_guest
id_guest = ''

global id_editor
id_editor = ''

global id_author
id_author = ''


def initDB():
    mycursor = mydb.cursor()
    # mycursor.execute('USE biblioteca')


def displayMainMenu():
    print('\n — — — —' + role + ' MENU — — — - \n')
    print(' 1. Login')
    print(' 2. Register User')
    print(' 3. List all Books')
    print(' 4. Search Books')
    if role == 'MANAGER':
        print(' 5. See All Users')
    if role == 'MANAGER':
        print(' 6. Delete user')
    if role == 'AUTHOR':
        print(' 5. List Your Books')
    if role != '':
        print(' 7. See your favourites and wishlist in matter of books')
    print(' 8. Send a message')
    print(' 9. Exit')
    print('\n — — — — — — — — — — \n')


def loginUser():
    mycursor = mydb.cursor()
    print(' — — — User Login — — — \n')
    # email = input('Enter email: \t')
    # pss = input('Enter password: \t')
    # email = 'george.vrinceanu@staff.tuiasi.ro'
    # pss = 'test_pss'
    email = 'test.author@student.tuiasi.ro'
    pss = 'narc'
    sql_select_user = 'SELECT id, role_id FROM users WHERE email = %s and password = %s'
    val = (email, pss)
    mycursor.execute(sql_select_user, val)
    myresult = mycursor.fetchall()

    if len(myresult) > 0:
        print(' — — — SUCCESS — — — ')
        global role
        global id_manager
        global id_editor
        global id_author
        global id_guest

        if myresult[0][1] == 0:
            id_manager = myresult[0][0]
            role = 'MANAGER'
        elif myresult[0][1] == 1:
            id_editor = myresult[0][0]
            role = 'EDITOR'
        elif myresult[0][1] == 2:
            id_author = myresult[0][0]
            role = 'AUTHOR'
        else:
            id_guest = myresult[0][0]
            role = 'GUEST'

        print('You just logged in as ' + role)
        run()
    else:
        print('Wrong credentials')
        loginUser()


def registerUser():
    mycursor = mydb.cursor()

    print(' — — — User Registration — — — \n')
    fname = input('Enter firstname: ')
    lname = input('Enter lastname: ')
    pss = input('Enter password: ')
    email = input('Enter email: ')
    tel = input('Enter telephone: ')

    req_role = int(input(
        'Do you request for a special role? \n\t\t Yes - Press 1 for Editor / Press 2 for Author \n\t\t No - Press 3 '
        'or 9 if you don\'t want a special role'))
    sw_role = 1

    while sw_role == 1:
        if req_role != 1 and req_role != 2 and req_role != 3 and req_role != 9:
            req_role = int(input(
                'Do you request for a special role? \n\t\t Yes - Press 1 for Editor / Press 2 for Author \n\t\t No - '
                'Press 3 or 9 if you don\'t want a special role'))
            sw_role = 1
        else:
            sw_role = 0
            break

    sql_insert_user = 'INSERT INTO users(role_id, first_name, last_name, password, email, telephone, request_role) ' \
                      'VALUES (%s, %s, %s, %s, %s, %s, %s) '
    values_user = ('3', fname, lname, pss, email, tel, req_role)
    mycursor.execute(sql_insert_user, values_user)

    mydb.commit()
    print(' — — — SUCCESS — — — \n')
    run()


def getAllBooks():
    mycursor = mydb.cursor()

    print(' — — — List All Books — — — \n')
    sql_select_books = 'SELECT books.title, CONCAT(users.first_name, " ", users.last_name) author_name, books.genre, ' \
                       'books.year FROM users, books WHERE users.id = books.author_id AND users.role_id = 2 '
    mycursor.execute(sql_select_books)

    myresult = mycursor.fetchall()

    print('{:^30}'.format('Title'), end=' ')
    print('{:^25}'.format('Author'), end=' ')
    print('{:^50}'.format('Genre'), end=' ')
    print('{:^27}'.format('Year'))

    for res in myresult:
        # print('Title: ' + res[0] + '\tAuthor: ' + res[1] + '\tGenre: ' + res[2] + '\tYear: ' + res[2])
        print('  {:<30} '.format(res[0]), end=' ')
        print('  {:<25} '.format(res[1]), end=' ')
        print('  {:<50} '.format(res[2]), end=' ')
        print('  {:<4} '.format(res[3]))

    print('\n\nDo you want to return to the main menu?')
    n = int(input('1 - Yes / 2 - No'))

    if n == 1:
        run()
    else:
        getAllBooks()


def searchBook():
    mycursor = mydb.cursor()

    print(' — — — Search in all Books — — — \n')
    search_attr = input(
        'You can search a book by author / genre / title / year\nIf you want to close the search, just type exit')

    sw_search_attr = 1

    while sw_search_attr == 1:
        if search_attr != 'author' and search_attr != 'genre' and search_attr != 'title' and search_attr != 'year' and search_attr != 'exit':
            search_attr = input(
                'You can search a book by author / genre / title / year\nIf you want to close the search, just type '
                'exit')
            sw_search_attr = 1
        else:
            sw_search_attr = 0
            break

    if search_attr == 'exit':
        print('You selected the ' + search_attr + ' option')
        run()
    elif search_attr == 'author':
        search_value = input('Select the author name')
        sql_search_books = 'SELECT books.title, CONCAT(users.first_name, " ", users.last_name) author_name, ' \
                           'books.genre, books.year FROM users, books WHERE users.id = books.author_id AND ' \
                           'users.role_id = 2 AND (users.first_name = %s OR users.last_name = %s) '
    else:
        search_value = input('Select the ' + search_attr)
        sql_search_books = 'SELECT books.title, CONCAT(users.first_name, " ", users.last_name) author_name, ' \
                           'books.genre, books.year FROM users, books WHERE users.id = books.author_id AND ' \
                           'users.role_id = 2 AND books.' + search_attr + '=%s '

    mycursor.execute(sql_search_books, search_value)

    myresult = mycursor.fetchall()

    print('{:^30}'.format('Title'), end=' ')
    print('{:^25}'.format('Author'), end=' ')
    print('{:^50}'.format('Genre'), end=' ')
    print('{:^27}'.format('Year'))

    for res in myresult:
        print('  {:<30} '.format(res[0]), end=' ')
        print('  {:<25} '.format(res[1]), end=' ')
        print('  {:<50} '.format(res[2]), end=' ')
        print('  {:<4} '.format(res[3]))

    print('\n\nDo you want to to return to the main menu?')
    n = int(input('1 - Yes / 2 - No'))

    if n == 1:
        run()
    else:
        searchBook()


def getAllUsers():
    mycursor = mydb.cursor()

    print(' — — — List All Users — — — \n')
    sql_select_all_users = 'SELECT id, CONCAT(first_name, " ", last_name) name, role_id, email, telephone, ' \
                           'request_role FROM users; '
    mycursor.execute(sql_select_all_users)

    myresult = mycursor.fetchall()

    requested_role_users_id = []
    requested_role_users_roles = []

    print('{:^7}'.format('Id'), end=' ')
    print('{:^22}'.format('Name'), end=' ')
    print('{:^22}'.format('Role'), end=' ')
    print('{:^36}'.format('Email'), end=' ')
    print('{:^28}'.format('Telephone'), end=' ')
    print('{:^14}'.format('Requested role'))

    for res in myresult:
        print('  {:<4} '.format(res[0]), end=' ')
        print('  {:<25} '.format(res[1]), end=' ')
        if res[2] == 0:
            current_role = 'manager'
        elif res[2] == 1:
            current_role = 'editor'
        elif res[2] == 2:
            current_role = 'author'
        else:
            current_role = 'guest'
        print('  {:<12} '.format(current_role), end=' ')
        print('  {:<40} '.format(res[3]), end=' ')
        print('  {:<20} '.format(res[4]), end=' ')
        if res[5] == 1:
            requested_role_users_id.append(res[0])
            requested_role_users_roles.append(res[5])

            requested_role = 'editor'
        elif res[5] == 2:
            requested_role_users_id.append(res[0])
            requested_role_users_roles.append(res[5])

            requested_role = 'author'
        else:
            requested_role = ''
        print('  {:<12} '.format(requested_role))

    print('\n\t{:>30}'.format('Do you want to offer a special role to an user?'))

    option = int(input('\t1 - Yes / 2 - No'))

    if option == 1:
        sw_update_user_role = 1

        while sw_update_user_role:
            user_id = int(input('Introduce id of the user:'))
            if user_id in requested_role_users_id:
                index = requested_role_users_id.index(user_id)

                sql_update_user_role = 'UPDATE users SET role_id = %s AND request_role = %s WHERE id = %s'
                values_requested_role = (requested_role_users_roles[index], '3', requested_role_users_id[index])
                mycursor.execute(sql_update_user_role, values_requested_role)
                mydb.commit()

                print(' — — — SUCCESSFULLY UPDATED — — — ')

                print('\nDo you want to offer a special role to another user?')
                n = int(input('1 - Yes / 2 - No'))
                if n == 1:
                    sw_update_user_role = 1
                else:
                    print('\n\nDo you want to return to the main menu?')
                    n = int(input('1 - Yes / 2 - No'))

                    if n == 1:
                        run()
                    else:
                        sw_update_user_role = 1
            else:
                sw_update_user_role = 1

    print('\n\nDo you want to return to the main menu?')
    n = int(input('1 - Yes / 2 - No'))

    if n == 1:
        run()
    else:
        getAllUsers()


def deleteUser():
    mycursor = mydb.cursor()

    print(' — — — Delete a user — — — \n')
    sql_select_all_users = 'SELECT id, CONCAT(first_name, " ", last_name) name, role_id, email, telephone FROM users WHERE role_id != \'0\';'
    mycursor.execute(sql_select_all_users)
    myresult = mycursor.fetchall()

    requested_delete_user = []

    print('{:^7}'.format('Id'), end=' ')
    print('{:^22}'.format('Name'), end=' ')
    print('{:^22}'.format('Role'), end=' ')
    print('{:^36}'.format('Email'), end=' ')
    print('{:^28}'.format('Telephone'))

    for res in myresult:
        requested_delete_user.append(res[0])
        print('  {:<4} '.format(res[0]), end=' ')
        print('  {:<25} '.format(res[1]), end=' ')
        if res[2] == 0:
            current_role = 'manager'
        elif res[2] == 1:
            current_role = 'editor'
        elif res[2] == 2:
            current_role = 'author'
        else:
            current_role = 'guest'
        print('  {:<12} '.format(current_role), end=' ')
        print('  {:<40} '.format(res[3]), end=' ')
        print('  {:<20} '.format(res[4]))

    print('\n\t{:>30}'.format('Do you want to delete an user?'))

    option = int(input('\t1 - Yes / 2 - No'))

    if option == 1:
        sw_delete_user = 1

        while sw_delete_user:
            user_id = int(input('Introduce id of the user:'))
            if user_id in requested_delete_user:

                sql_delete_user = 'DELETE FROM users WHERE id = %s'
                value_delete_user = int(user_id)
                mycursor.execute(sql_delete_user, (value_delete_user,))
                mydb.commit()

                print(' — — — SUCCESSFULLY DELETED — — — ')

                print('\nDo you want to delete another user?')
                n = int(input('1 - Yes / 2 - No'))
                if n == 1:
                    sw_delete_user = 1
                else:
                    print('\n\nDo you want to return to the main menu?')
                    n = int(input('1 - Yes / 2 - No'))

                    if n == 1:
                        run()
                    else:
                        sw_delete_user = 1
            else:
                sw_delete_user = 1

    print('\n\nDo you want to return to the main menu?')
    n = int(input('1 - Yes / 2 - No'))

    if n == 1:
        run()
    else:
        deleteUser()


def getAllBooksEditor():
    mycursor = mydb.cursor()

    print(' — — — List Your Books — — — \n')
    sql_select_books = 'SELECT books.id, books.editor_id, books.title, books.genre, books.year FROM books WHERE ' \
                       'books.author_id = %s '
    mycursor.execute(sql_select_books, (id_author,))

    myresult = mycursor.fetchall()

    author_books_id = []

    print('{:^8}'.format('Id Book'), end=' ')
    print('{:^25}'.format('Editor name'), end=' ')
    print('{:^25}'.format('Book Title'), end=' ')
    print('{:^50}'.format('Genre'), end=' ')
    print('{:^36}'.format('Year'))

    for res in myresult:
        author_books_id.append(res[0])
        print('  {:<10} '.format(res[0]), end=' ')
        print('  {:<20} '.format(res[1]), end=' ')
        print('  {:<30} '.format(res[2]), end=' ')
        print('  {:<50} '.format(res[3]), end=' ')
        print('  {:<4} '.format(res[4]))

    print('\n{:>30}'.format('Do you want to modify information of one of your books?'))

    option = int(input('1 - Yes / 2 - No\t'))

    if option == 1:
        sw_update_author_book = 1

        while sw_update_author_book:
            book_id = int(input('Introduce id of the book:\t'))
            if book_id in author_books_id:
                index = author_books_id.index(book_id)

                attribute_to_edit = input(
                    'Select what attribute do you want to edit: \n\t title / genre / year or cancel if you want to '
                    'exit:\t')

                sw_attribute = 1

                while sw_attribute == 1:
                    if attribute_to_edit != 'title' and attribute_to_edit != 'genre' and attribute_to_edit != 'year' and attribute_to_edit != 'cancel':
                        attribute_to_edit = input(
                            'Select what attribute do you want to edit: \n\t title / genre / year or cancel if you '
                            'want to exit:\t')
                        sw_attribute = 1
                    else:
                        sw_attribute = 0
                        break

                if attribute_to_edit != 'cancel':
                    value_edited_book = input('Insert the new value for ' + attribute_to_edit + ':\t')

                    sql_insert_edit_book = 'INSERT INTO books_edited(book_id, ' + attribute_to_edit + ') VALUES (%s, %s)'
                    values_edited_book = (book_id, value_edited_book)
                    mycursor.execute(sql_insert_edit_book, values_edited_book)
                    mydb.commit()

                    sql_update_author_book = 'UPDATE books SET status = "request_changes" WHERE id = %s'
                    mycursor.execute(sql_update_author_book, (book_id,))
                    mydb.commit()

                    print('\n — — — SUCCESSFULLY REQUESTED UPDATE — — — \n')

                if attribute_to_edit != 'cancel':
                    print('Do you want to edit another book?')
                    n = int(input('1 - Yes / 2 - No\t'))
                else:
                    n = 0

                if n == 1:
                    sw_update_author_book = 1
                else:
                    print('\n\nDo you want to return to the main menu?')
                    n = int(input('1 - Yes / 2 - No\t'))

                    if n == 1:
                        run()
                    else:
                        sw_update_author_book = 1
            else:
                sw_update_author_book = 1

    print('\n\nDo you want to return to the main menu?')
    n = int(input('1 - Yes / 2 - No\t'))

    if n == 1:
        run()
    else:
        getAllBooksEditor()

def getFavouriteAndWishlist():
    mycursor = mydb.cursor()
    id_user = ''

    if id_manager != "":
        id_user = id_manager
    if id_editor != "":
        id_user = id_editor
    if id_author != "":
        id_user = id_author
    if id_guest != "":
        id_user = id_guest

    favourite_books = []
    wishlist_books = []

    myquery = {"id": id_user}
    mydoc = users_coll.find(myquery)

    for x in mydoc:
        favourite_books = x['favourite_books']
        wishlist_books = x['wishlist']

    print(favourite_books)
    # print(wishlist_books)

    myresult_favourite = []
    myresult_wishlist = []

    for y in favourite_books:
        sql_select_books = 'SELECT CONCAT(users.first_name, " ", users.last_name), books.title, books.genre, books.year FROM books, users WHERE books.id = %s AND books.author_id = users.id'
        mycursor.execute(sql_select_books, (y,))

        myresult = mycursor.fetchall()
        for res in myresult:
            myresult_favourite.append(res)

    for y in wishlist_books:
        sql_select_books = 'SELECT CONCAT(users.first_name, " ", users.last_name), books.title, books.genre, books.year FROM books, users WHERE books.id = %s AND books.author_id = users.id'
        mycursor.execute(sql_select_books, (y,))

        myresult = mycursor.fetchall()
        for res in myresult:
            myresult_wishlist.append(res)

    print('\n — — — Your Favourites books  — — — \n')
    for res_fav in myresult_favourite:
        print(res_fav)

    print('\n -— — — Your Wishlist books  — — — \n')

    for res_wish in myresult_wishlist:
        print(res_wish)

    run()

def exit():
    n = int(input("Press 9 to exit : "))
    if n == 9:
        mydb.close()
    else:
        print("Invalid Option")
        exit()


def run():
    print("run print: " + role)
    displayMainMenu()
    n = int(input('Enter option : '))
    if n == 1:
        loginUser()
    elif n == 2:
        registerUser()
    elif n == 3:
        getAllBooks()
    elif n == 4:
        searchBook()
    elif n == 5 and role == 'MANAGER':
        getAllUsers()
    elif n == 6 and role == 'MANAGER':
        deleteUser()
    elif n == 5 and role == 'AUTHOR':
        getAllBooksEditor()
    elif n == 7 and role != '':
        getFavouriteAndWishlist()
    elif n == 9:
        print(' — — — Thank You — — -')
        sys.exit()
    else:
        run()


if __name__ == '__main__':
    initDB()
    run()
