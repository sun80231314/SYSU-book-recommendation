# -*- coding: utf-8 -*-

class Book(object):
    """Model for Book"""
    def __init__(self, uid, name, imgUrl,
      isbn='', author='', press='', doubanPoint=0, doubanRateSum=0,
      bookDesciption='', authorDesciption='', sysuLibUrl=''):
        super(Book, self).__init__()
        # Majar infomations
        self.uid = uid
        self.name = name
        self.imgUrl = imgUrl
        # More details
        self.isbn = isbn
        self.author = author
        self.press = press
        self.doubanPoint = doubanPoint
        self.doubanRateSum = doubanRateSum
        self.bookDesciption = bookDesciption
        self.authorDesciption = authorDesciption
        self.sysuLibUrl = sysuLibUrl

