from connect import *
from tabulate import tabulate
from User import *


def user_exist (username) :
    users=  sql('select distinct username  from users')
     
    
    if username in users[users.columns[0]].values.tolist():
        return True
    return False
    
    
    
    
    
    
    
def sign_up(username):
    if not user_exist(username) :
        cmd=f"insert into users (username) values ('{username}') "
        sql(cmd)
        print('added!')
    else :
        print ('user already exists')


        
def search_by_author(author)   : 
    return sql(f"SELECT * FROM books where author='{author}'")
    

def recently_added(*genre):
    if len(genre) ==0 : 
        return sql (f"SELECT * FROM books limit 5")
    else:
        genre=list(genre)[0]
        return sql(f"select * from books where genre='{genre}' limit 5 ")
    
def most_read_books(*genre) :
    if len(genre) ==0 : 
            return sql (f"""

                select x.count , books.* from 
                (select b.book_id  , sum (a.read) as count from
                 (select * from books) b
                 inner join 
                (select book_id,read from users where read is not null) a ON a.book_id=b.book_id
                GROUP BY b.book_id ) x inner join books  ON x.book_id=books.book_id limit 10

                    
                    """)
    else:
        genre=list(genre)[0]
        return sql(f"""
                  

            select x.count , books.* from 
            (
            select b.book_id  , sum (a.read) as count from
             (select * from books where genre='{genre}' ) b
             inner join 
            (select book_id,read from users where read is not null) a ON a.book_id=b.book_id
            GROUP BY b.book_id ) x inner join books  ON x.book_id=books.book_id limit 10
        """)
def  most_favorite_books (*genre) :
    if len(genre) ==0 : 
            return sql (f"""

                select x.count , books.* from 
                (select b.book_id  , sum (a.fav) as count from
                 (select * from books) b
                 inner join 
                (select book_id,fav from users where fav is not null) a ON a.book_id=b.book_id
                GROUP BY b.book_id ) x inner join books  ON x.book_id=books.book_id limit 10

                    
                    """)
    else:
        genre=list(genre)[0]
        return sql(f"""
                  

            select x.count , books.* from 
            (
            select b.book_id  , sum (a.fav) as count from
             (select * from books where genre='{genre}' ) b
             inner join 
            (select book_id,fav from users where fav is not null) a ON a.book_id=b.book_id
            GROUP BY b.book_id ) x inner join books  ON x.book_id=books.book_id limit 10
        """)
    
    
    
def most_read_genres   ():
    return sql ("""

    select g.genre, sum (u.read) as count FROM 
     ( select genre, book_id from books ) g 
     inner join 
     (select read, book_id from users  where read is not null) u ON g.book_id=u.book_id
    GROUP BY genre ORDER BY count DESC LIMIT 5
    """)
def most_read_authors () :
     return sql ("""

    select g.author, sum (u.read) as count FROM 
     ( select author, book_id from books ) g 
     inner join 
     (select read, book_id from users  where read is not null) u ON g.book_id=u.book_id
    GROUP BY author ORDER BY count DESC LIMIT 5
    """)

def borrow_book (book_id, username) : 
    if user_exist :
        quantity =  (sql(f"SELECT quantity FROM BOOKS WHERE BOOK_ID='{book_id}' ") ._get_value(0, 0, takeable=False)  )
        if quantity >0 : 
            #make sure the user hasn't borrowed the same book :
            b= sql (f"SELECT * FROM users WHERE  book_id = {book_id} AND username = '{username}' AND borrowed =1")
            print (b)
            print(  len(b.index))
            if len(b.index)  == 0 : 
            #adding a row to users
                sql(f"INSERT INTO users (username,book_id,  borrowed) VALUES ( '{username}' , {book_id}, 1)")
                sql (f"UPDATE books SET quantity = {quantity-1} WHERE book_id = {book_id}  ")
                print ('Book borrowed !')
            else:  
                print ('Book already borrowed!')
 
def return_book (book_id, username) : 
    if user_exist :
            quantity =  (sql(f"SELECT quantity FROM BOOKS WHERE BOOK_ID='{book_id}' ") ._get_value(0, 0, takeable=False)  )
            
        
            #make sure that the book is borrowed :  
            b= sql (f"SELECT * FROM users WHERE  book_id = {book_id} AND username = '{username}' and borrowed =1")
            if len(b.index) > 0 : 
            #adding a row to users
                sql (f"UPDATE users SET borrowed =0 WHERE book_id = {book_id}  ")
                sql (f"UPDATE books SET quantity = {quantity+1} WHERE book_id = {book_id}  ")
                print ('Book returned!')
            else:  
                print ('Book is not borrowed!')    


    
def mark_read (book_id, username)  :
    if user_exist (username) :
            
            mr= sql (f"SELECT * FROM users WHERE  book_id = {book_id} AND username = '{username}' and read =1")
            if len(mr.index) == 0 : 
              sql(f"INSERT INTO users (username,book_id, read) VALUES ( '{username}', {book_id}, 1)")
            else:
                print('Book marked as read before!')


def mark_reading   (book_id, username) :
    if user_exist (username) :
            
            r= sql (f"SELECT * FROM users WHERE  book_id = {book_id} AND username = '{username}' and reading =1")
            if len(r.index) == 0 : 
              sql(f"INSERT INTO users (username,book_id, reading) VALUES ('{username}', {book_id}, 1)")
            else:
                print('Book marked as reading before!')

def mark_will_read   (book_id, username) :
 
    if user_exist (username) :
            
            wr= sql (f"SELECT * FROM users WHERE  book_id = {book_id} AND username = '{username}' and will_read =1")
            if len(wr.index) == 0 : 
              sql(f"INSERT INTO users (username,book_id,  will_read) VALUES ( '{username}', {book_id}, 1)")
            else:
                print('Book marked as will read before!')
    
def fav_book ( book_id, username) :
     if user_exist (username) :
            #make sure the same book is not marked fav before:
            f= sql (f"SELECT * FROM users WHERE  book_id = {book_id} AND username = '{username}' and fav =1")
            if len(f.index) == 0 : 
              sql(f"INSERT INTO users (username,book_id,  fav) VALUES ( '{username}' , {book_id}, 1)")
            else:
                print('Book marked as favourite before!')
    
def my_books(username)    :
  if user_exist (username) :
    books_you_read = sql (f"""SELECT b.* FROM (SELECT * FROM users WHERE  username = '{username}' and read =1) u 
    inner join books b ON u.book_id=b.book_id """)
    
    reading = sql (f"""SELECT b.* FROM (SELECT * FROM users WHERE  username = '{username}' and reading =1) u 
    inner join books b ON u.book_id=b.book_id """)                      
                    
    will_read = sql (f"""SELECT b.* FROM (SELECT * FROM users WHERE  username = '{username}' and will_read =1) u 
    inner join books b ON u.book_id=b.book_id """)       
    
    fav = sql (f"""SELECT b.* FROM (SELECT * FROM users WHERE  username = '{username}' and fav =1) u 
    inner join books b ON u.book_id=b.book_id """)
    

    print ('Books you read:' , '\n',table (books_you_read ) )   
    print ('Books you are reading: ' , '\n',table (reading) )   
    print ('Books you will_read: ' , '\n',table(will_read) )   
    print ('Your favourite books are: ' , '\n',table(fav) ) 
     
    
    
    
def statistics (username)  :
     if user_exist (username) :
        books_you_read = sql (f"""SELECT b.* FROM (SELECT * FROM users WHERE  username = '{username}' and read =1) u 
        inner join books b ON u.book_id=b.book_id """)

        reading = sql (f"""SELECT b.* FROM (SELECT * FROM users WHERE  username = '{username}' and reading =1) u 
        inner join books b ON u.book_id=b.book_id """)                      

        will_read = sql (f"""SELECT b.* FROM (SELECT * FROM users WHERE  username = '{username}' and will_read =1) u 
        inner join books b ON u.book_id=b.book_id """)       

        fav = sql (f"""SELECT b.* FROM (SELECT * FROM users WHERE  username = '{username}' and fav =1) u 
        inner join books b ON u.book_id=b.book_id """)

        stats= { 'Books you read:'  : len(books_you_read.index ), 
         'Books you are reading: ': len(reading.index) ,   
         'Books you will_read: ' : len(will_read.index) ,  
         'Your favourite books are: ': len(fav.index) ,  

        }
        for i in stats.items():
            print (i)
     
def table (df)    :
    return tabulate(df, tablefmt="outline") 
    
 

def select_random_user ():
    users=sql('select username from users')
    r=random.randrange(1,len (users))
    username=(users.iloc[:,[0]].values[r])[0]
    print (username)
    return username

def select_random_book_id ():
    books = sql('select book_id from books')
    r=random.randrange(1,len (books))
    book=(books.iloc[:,[0]].values[r])[0]
    print (book)
    return book

def make_random_operation ():
    username = select_random_user ()
    book=select_random_book_id ()
    operation = random.randrange(1,7)
    if operation ==1:
     print ('going to borrow_book ')
     borrow_book (book, username)
     
    elif operation ==2:
     print ('going to return_book')
     return_book(book, username)
    elif operation ==3: 
     print ('going to mark_read')
     mark_read(book, username)
    elif operation ==4: 
     print ('going to mark_will_read ')
     mark_will_read(book, username)
    elif operation ==5:
        print ('going to mark_reading ')
        mark_reading(book, username)
    elif operation ==6:
        print ('going to fav_book')
        fav_book(book, username)
    



# for i in range (100) :
#     sign_up(generate_random_user () )
# for i in range (100) : 
#     make_random_operation ()
# print (select_random_book_id ())
# print (sql('select * from users ORDER BY username limit 5'))
# make_random_operation ()
# select_random_book_id ()
# statistics (select_random_user())
my_books('Silas_Molly_3583')
# print (sql( "select * from users where username ='Lauryn_Judi_2410'" ))