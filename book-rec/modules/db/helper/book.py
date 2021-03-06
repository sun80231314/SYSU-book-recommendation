# -*- coding: utf-8 -*-

from modules.db.models.book import Book
from modules.db.helper import mysqlConn

@mysqlConn
def getPopularBooks(quantity=10, cur=None, conn=None):
    '''Get the most popular books.

    Determine polularity in according to doubanRatesum.
    :Param quantity: Number of returned books.
    :Return: A list of Book object.
    '''
    sql = '''select uid, name, imgUrl from book order by doubanRateSum desc 
        limit %s'''
    num = cur.execute(sql, quantity)
    records = cur.fetchmany(num)
    books = []
    for rec in records:
        books.append(Book(rec[0], rec[1], rec[2]))
    return books

@mysqlConn
def getRecommendedBooks(userToken, cur, conn):
    '''Get 20 recommended books at most which is ordered by relevance.

    Recommended books are generated by outer systems.
    :Param userToken: The token which identifies a user.
    :Return: A list of Book object.
    '''
    sql = '''select recBooks from user where token = %s'''
    cur.execute(sql, userToken)
    record = cur.fetchone()
    if not record:
        # If a user visited this site for the first time, no recommended
        # book exists.
        return getPopularBooks(30)[10:]
        # return getPopularBooks(5)[2:]
    bookUids = '(%s)' % record
    sql = '''select uid, name, imgUrl from book where uid in %s''' % bookUids
    num = cur.execute(sql)
    records = cur.fetchmany(num)
    books = []
    for rec in records:
        books.append(Book(rec[0], rec[1], rec[2]))
    return books

@mysqlConn
def searchBooks(word, page, size, cur, conn):
    startIndex = page * size
    word = '%' + '%'.join(word) + '%'
    sql = '''select uid, name, imgUrl from book
        where name like %s or author like %s
        limit %s, %s'''
    num = cur.execute(sql, (word, word, startIndex, size))
    records = cur.fetchmany(num)
    books = []
    for rec in records:
        books.append(Book(rec[0], rec[1], rec[2]))
    return books

@mysqlConn
def getBookDetail(bookUid, cur, conn):
    '''Return a Book object with full infomation.
    '''
    sql = '''select uid, name, imgUrl, isbn, author, press, doubanPoint,
        doubanRateSum, bookDescription, authorDescription, sysuLibUrl
        from book where uid = %s'''
    cur.execute(sql, bookUid)
    rec = list(cur.fetchone())
    for index in range(len(rec)):
        if rec[index] is None:
            rec[index] = ''
    return Book(*rec)

@mysqlConn
def getRelevantBooks(bookUid, cur, conn):
    # sql = '''select relevantBooks from book where uid = %s'''
    # cur.execute(sql, bookUid)
    # record = cur.fetchone()[0]
    # bookUids = '(%s)' % record
    # sql = '''select uid, name, imgUrl from book where uid in %s''' % bookUids
    # num = cur.execute(sql)
    # records = cur.fetchmany(num)
    # books = []
    # for rec in records:
    #     books.append(Book(rec[0], rec[1], rec[2]))
    # return books
    return getPopularBooks(100)[90:]

@mysqlConn
def getBooksByLabel(labelName, page, size, order='doubanRateSum',
  cur=None, conn=None):
    # get labelUid
    sql = '''select uid from bookLabel where name = %s'''
    cur.execute(sql, labelName)
    labelUid = cur.fetchone()
    if not labelUid:
        # labelName doesn't exist.
        return []
    labelUid = labelUid[0]
    if order not in ['doubanRateSum']:
        order = 'doubanRateSum'
    startIndex = page * size
    sql = '''select book.uid, book.name, book.imgUrl from labelOfBook inner join
        book on book.uid = labelOfBook.bookUid where labelOfBook.bookLabelUid =
        %s order by book.{} desc limit %s, %s'''.format(order)
    num = cur.execute(sql, (labelUid, startIndex, size))
    records = cur.fetchmany(num)
    books = []
    for rec in records:
        books.append(Book(rec[0], rec[1], rec[2]))
    return books

@mysqlConn
def incBookViewCount(userToken, bookUid, cur, conn):
    # Assume bookUid is valid.
    sql = '''select uid from user where token = %s'''
    cur.execute(sql, userToken)
    rec = cur.fetchone()
    if not rec:
        return
    userUid = rec[0]
    sql = '''select viewCount from userBookView where userUid = %s and 
        bookUid = %s'''
    cur.execute(sql, (userUid, bookUid))
    record = cur.fetchone()
    if not record:
        sql = '''insert into userBookView(userUid, bookUid, viewCount)
            values(%s, %s, 1)'''
    else:
        sql = '''update userBookView set viewCount = viewCount + 1 
            where userUid = %s and bookUid = %s'''
    cur.execute(sql, (userUid, bookUid))
    conn.commit()

@mysqlConn
def getBookSum(cur, conn):
    sql = '''select count(*) from book'''
    cur.execute(sql)
    bookSum = cur.fetchone()[0]
    return bookSum

@mysqlConn
def getBookSumOfLabel(labelName, cur, conn):
    # sql = '''select count(*) from labelOfBook inner join bookLabel 
    #       on labelOfBook.bookLabelUid = bookLabel.uid
    #       where bookLabel.name = %s'''
    sql = '''select useCount from bookLabel where name = %s'''
    cur.execute(sql, labelName)
    bookSum = cur.fetchone()[0]
    return bookSum

@mysqlConn
def getBookLabels(bookUid, cur, conn):
    sql = '''select bookLabel.name from labelOfBook inner join bookLabel
          on labelOfBook.bookLabelUid = bookLabel.uid
          where labelOfBook.bookUid = %s '''
    num = cur.execute(sql, bookUid)
    records = cur.fetchmany(num)
    labels = [rec[0] for rec in records]
    return labels
