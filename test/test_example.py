import pytest


def test_equal_or_not_equal_to():
    """Simple equality and inequality assertions.

    These tests show the basic use of `==` and `!=` in assertions.
    They are intentionally trivial — the goal is to demonstrate test syntax
    and the difference between equality and inequality checks.
    """
    assert 3 == 3
    assert 3 != 1


def test_type():
    """Demonstrate type-related checks.

    Note: the original code used `type('hello world' is str)` which is
    incorrect because `'hello world' is str` evaluates to a boolean first.
    Here we keep the intent (showing type checks) but use `isinstance` or
    direct `type(...) is ...` for clarity.
    """
    # Prefer `isinstance` for type checks in production code; here we show `type(...) is ...` as an exact type match.
    assert type('hello world') is str
    assert type('10') is not int


def test_less_than_greater_than():
    """Numeric comparison examples: greater-than and less-than."""
    assert 3 > 1
    assert 1 < 2


def test_list():
    """Examples working with lists and the built-in `any`/`all` helpers.

    - `in` / `not in` test membership
    - `any(iterable)` returns True if any element is truthy
    - `all(iterable)` returns True if all elements are truthy
    """
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]

    # Membership assertions
    assert 1 in num_list
    assert 7 not in num_list

    # `any_list` contains only falsy values, so `any(any_list)` is False
    assert not any(any_list)

    # All elements in `num_list` are non-zero (truthy), so `all(...)` is True
    assert all(num_list)


def test_boolean():
    """Boolean identity and negation examples.

    Use `is True` / `is not` to show identity comparisons with boolean constants.
    """
    validated = True

    # `is True` checks identity with the singleton True — commonly used in tests for clarity
    assert validated is True

    # The expression ('hello' == 'world') evaluates to False; comparing it with `is not validated` demonstrates negation
    assert ('hello' == 'world') is not validated


def test_instance():
    """Show how to use `isinstance` correctly.

    `isinstance(obj, Type)` is preferred over comparing types directly in many cases
    because it supports subclass checks.
    """
    assert isinstance('hello world', str)  # True: 'hello world' is a str
    assert not isinstance('10', int)  # False: '10' is a string, not an int


class Student:
    """Small helper class used by the fixture and initialization test.

    Attributes mirror a simple data model for a student: first/last name, major, and years.
    """

    def __init__(self, first_name: str, Last_name: str, major: str, years: int):
        # keep attribute assignment unchanged to avoid breaking tests that rely on these names
        self.first_name = first_name
        self.last_name = Last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    """Pytest fixture that returns a default `Student` instance for reuse in tests.

    Fixtures provide a clean way to set up common test data or environment once and
    inject it into multiple tests by name. Here it's used to provide a sample Student.
    """
    return Student('John', 'doe', 'Computer Science', 3)


def test_person_initialization(default_employee):
    """Verify the `Student` object returned by the fixture is initialized correctly."""
    assert default_employee.first_name == 'John'
    assert default_employee.last_name == 'doe'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 3