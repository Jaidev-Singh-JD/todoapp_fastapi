def test_equal_or_not_equal_to():
    assert 3 == 3
    assert 3!=1

def test_type():
    assert type('hello world' is str)
    assert type('10' is not int)

def test_less_than_greater_than():
    assert 3 > 1
    assert 1 < 2

def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False , False]

    assert 1 in num_list
    assert 7 not in num_list

    # Definition: any(iterable)
    #Returns True if at least one element in the iterable is truthy.
    #Returns False if all elements are falsy.
    assert not any(any_list)

    assert all(num_list)  # passes (all numbers are non-zero → truthy)


def test_boolean():
    validated = True

    assert validated is True
    assert ('hello' == 'world') is not validated


def test_instance():
    assert isinstance ('hello world', str)     #Checks if 'hello world' is an instance of str.
    assert not isinstance ('10', int )     #isinstance('10', int) → False (since '10' is a string, not an integer).