from connect import *



def user_exist (username) :
    users=  sql('select distinct username  from users')
    username= (username,)
    
    if username in users:
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
    pass
#         -control user (make sure it exists or not , if not > msg)
#         -if book avalable : 
#             add a row to users , with username + borrowed =1
#             change the quzntity of the book by -1
    
def return_book (book_id, username) : 
    pass
#     after controling user : 
#         search for book_id + username in users 
#         if borowed is 1 > change it to null ? ( or delete row ? )
#         change the quzntity of the book by +1
    
def mark_read (book_id, username)  :
    sql(f""" select b.book_id, string_agg(p.username, ';')
                    from books b 
                    join users p on ( b.book_id = p.read) where username=('{username}') 
                    group by 1 """)

    for book_id in sql:
        print(f'The ‘BOOK ID’ {book_id} this book as “read” ')
    
    
    sql(f"SELECT SUM(will_read) FROM users WHERE username= ('{username}')")
    
    for book_id in sql:
        print(f'You mark read {book_id} will_read')
#     control user cresult
#     add a row to users : with book id + username + read=1

def mark_reading   (book_id, username) :
    sql(f""" select b.book_id, string_agg(p.username, ';')
                    from books b 
                    join users p on ( b.book_id = p.reading) where username=('{username}') 
                    group by 1 """)

    for book_id in sql:
        print(f'The ‘BOOK ID’ {book_id} this book as “reading” ')
    
    
    sql(f"SELECT SUM(will_read) FROM users WHERE username= ('{username}')")
    
    for book_id in sql:
        print(f'You mark read {book_id} as reading')


def mark_will_read   (book_id, username) :
    sql(f""" select b.book_id, string_agg(p.username, ';')
                    from books b 
                    join users p on ( b.book_id = p.will_read) where username=('{username}') 
                    group by 1 """)

    for book_id in sql:
        print(f'The ‘BOOK ID’ {book_id} this book as “will_read” ')
    
    
    sql(f"SELECT SUM(will_read) FROM users WHERE username= ('{username}')")
    
    for book_id in sql:
        print(f'You mark read {book_id} will_read')
    
    
def fav_book (  username) :
    pass
#      same logic for the previous, make fav=1
    
def my_books (username)    :
    pass
#     in users : search for everything related to this user
#     return  only rows where reading or read or will_read    are not null



def statistics (username) :
    pass
#     in users : search for everything related to this user WHERE read is not null + inner join with books ON book_id
        
#     now , for books_you_read :  group the results by book id ? 
#     use join in similar way to find all other statistics,
#     find a way to display results
        
    
    
 
  

# sql('select * from books')
# search_by_author("Suzanne collins")
# recently_added ('Science fiction')
# most_read_books('Science fiction')
# # most_favorite_books ()
# most_read_genres   ()
print (most_read_authors ())