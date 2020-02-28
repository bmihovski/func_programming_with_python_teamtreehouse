import json
from copy import copy
from functools import reduce, partial
from operator import attrgetter, itemgetter


class Book:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.title

    def __repr__(self):
        return str(self)


def get_books(filename, raw=False):
    try:
        data = json.load(open(filename))
    except FileNotFoundError:
        return []
    else:
        if raw:
            return data['books']
        return [Book(**book) for book in data['books']]


BOOKS = get_books('books.json')

RAW_BOOKS = get_books('books.json', raw=True)


# pub_sort = sorted(RAW_BOOKS, key=itemgetter('publish_date'))
# pages_sort = sorted(BOOKS, key=attrgetter('number_of_pages'))
# print(pub_sort[0]['publish_date'], pub_sort[-1]['publish_date'])
# print(pages_sort[0].number_of_pages, pages_sort[-1].number_of_pages)
### MAP ###
def sales_price(book):
    """
        Apply a 20% discount to the book's price
    """
    book = copy(book)
    book.price = round(book.price - book.price * .2, 2)
    return book


sales_books = map(sales_price, BOOKS)


# print(BOOKS[0].price)
# print(list(sales_books)[0].price)

### FILTER ###


def is_long_book(book):
    """
        Does a book have 600 pages?
    """

    return book.number_of_pages >= 600


long_books = filter(is_long_book, BOOKS)


# print(len(BOOKS))
# print(len(list(long_books)))


### CHAINING ###


def has_roland(book):
    return any(["Roland" in subject for subject in book.subjects])


def titlecase(book):
    book = copy(book)
    book.title = book.title.title()
    return book


# print(list(map(titlecase, filter(has_roland, BOOKS))))

def is_good_deal(book):
    return book.price <= 5


cheap_books = sorted(
    filter(is_good_deal, map(sales_price, BOOKS)),
    key=attrgetter('price')
)


# print(cheap_books[0])


### REDUCE ###


def add_book_prices(book1, book2):
    return book1 + book2


total = reduce(add_book_prices, [b.price for b in BOOKS])


# print(total)


def long_total(a=None, b=None, books=None):
    """Reduce representation"""
    if a is None and b is None and books is None:
        return None
    if a is None and b is None and books is not None:
        a = books.pop(0)
        b = books.pop(0)
        return long_total(a, b, books)
    if a is not None and books and b is None and books is not None:
        b = books.pop(0)
        return long_total(a, b, books)
    if a is not None and b is not None and books is not None:
        return long_total(a + b, None, books)
    if a is not None and b is not None and books is None:
        return long_total(a + b, None, None)
    if a is not None and b is None and not books or books is None:
        return a


# print(long_total(None, None, [b.price for b in BOOKS]))

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


# print(factorial(5))

### LAMBDA ###


total = reduce(lambda x, y: x + y, [b.price for b in BOOKS])
long_books = filter(lambda book: book.number_of_pages >= 600, BOOKS)
good_deals = filter(lambda book: book.price <= 6, BOOKS)
#print(len(list(good_deals)))


### PARTIALS ###

def mark_down(book, discount):
    book = copy(book)
    book.price = round(book.price - book.price * discount, 2)
    return book


standard = partial(mark_down, discount=.2)
#print(standard(BOOKS[0]).price)
half = partial(mark_down, discount=.4)
half_price_long_books = map(half, filter(is_long_book, BOOKS))
#print(list(half_price_long_books))


### CURRYING ###

def curried_f(x, y=None, z=None):
    def f(x, y, z):
        return x ** 3 + y ** 2 + z

    if y is not None and z is not None:
        return f(x, y, z)
    if y is not None:
        return lambda z: f(x, y, z)

    return lambda y, z=None: (
        f(x, y, z) if (y is not None and z is not None)
        else (lambda z: f(x, y, z))
    )


print(curried_f(2, 3, 4))
first_func = curried_f(2)
print(first_func)
second_func = first_func(3)
print(second_func)
third_func = second_func(4)
print(third_func)

