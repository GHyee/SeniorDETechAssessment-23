from typing import Tuple, List, Optional
from datetime import datetime
import hashlib


def has_correct_digits(number: int, num_digits: int = 8) -> bool:
    """
    Returns True if the given number has the specified number of digits,
    and False otherwise. By default, the expected number of digits is 8.

    Args:
        number (int): An integer representing the mobile number.
        num_digits (int): The expected number of digits (default 8).

    Returns:
        bool: True if the number has the correct number of digits, False otherwise.

    Example:
        >>> has_correct_digits(12345678)
        True
        >>> has_correct_digits(123456789, num_digits=10)
        True
        >>> has_correct_digits(123456789)
        False
    """
    # Convert the number to a string and count the number of digits
    num_digits_actual = len(str(number))

    # Return True if the number has the expected number of digits, False otherwise
    return num_digits_actual == num_digits


def identify_date_format(date_str: str) -> str:
    """
    Identifies the format of a date string.

    Args:
        date_str: A string containing a date in an unknown format.

    Returns:
        A string representing the format of the date string, or None if the format
        could not be identified.
    """
    # As the local date format is usually date at the front or the end,
    # we will assume dates such as 11/05/1999 to be dd-mm-yyyy instead of mm-dd-yyyy
    possible_formats = ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y", "%Y%m%d", "%d%m%Y",
                        "%m-%d-%Y", "%m%d%Y", "%m/%d/%Y"]

    for fmt in possible_formats:
        try:
            datetime.strptime(date_str, fmt)
            return fmt
        except ValueError:
            pass

    return None


def format_date_of_birth(dob_str: str, dob_format: str, output_format: str = "%Y%m%d") -> str:
    """
    Convert a date string in the specified format to YYYYMMDD format.

    Args:
        dob_str (str): Date string in the specified format.
        dob_format (str): Date format of the input date string.
        output_format (str): Optional parameter specifying the output date format.
            Default is "%Y%m%d" (YYYYMMDD format).

    Returns:
        str: Date of birth string in YYYYMMDD format.

    Raises:
        ValueError: If the date string cannot be parsed using the specified format.
    """
    dob = datetime.strptime(dob_str, dob_format)
    return dob.strftime(output_format)


def is_above_age(date_of_birth: str, age_cutoff: int, date_cutoff: str = "2022-01-01") -> bool:
    """
    Determines if an applicant is above a certain age as of a given date based on their date of birth.

    Args:
        date_of_birth: A string in YYYYMMDD format representing the applicant's date of birth.
        age_cutoff: An integer representing the minimum age required.
        date_cutoff: A string representing the date in YYYY-MM-DD format to compare the applicant's age against.
                     Defaulted to "2022-01-01".

    Returns:
        A boolean value indicating whether the applicant is at least the specified age as of the given date.
    """
    dob = datetime.strptime(date_of_birth, "%Y%m%d")
    cutoff_date = datetime.strptime(date_cutoff, "%Y-%m-%d")
    age = cutoff_date.year - dob.year - ((cutoff_date.month, cutoff_date.day) < (dob.month, dob.day))

    return age >= age_cutoff


def is_valid_email(email: str, suffixes: Optional[List[str]] = None) -> bool:
    """
    Checks if the email has a valid suffix and contains "@".

    Args:
        email (str): The email address to check.
        suffix (Optional[List[str]]): List of valid suffixes. Defaults to [".com", ".net"].

    Returns:
        bool: True if email has a valid suffix and contains "@"; False otherwise.
    """
    if suffixes is None:
        suffixes = [".com", ".net"]
    if "@" not in email:
        return False
    for s in suffixes:
        if email.endswith(s):
            return True
    return False


def is_empty_name(name: str) -> bool:
    """
    Check if the given name is empty or doesn't exist.

    Args:
        name: The name to check.

    Returns:
        True if the name is empty or doesn't exist, False otherwise.
    """
    if name is None or name.strip() == '':
        return True
    return False


def split_name(full_name: str) -> Tuple[str, str]:
    """
    Splits a full name into first and last name.

    Args:
        full_name (str): A string containing the full name, which may include a salutation and/or a suffix.

    Returns:
        tuple: A tuple containing the first and last name extracted from the full name.

    Example:
        >>> name = 'Dr. Jane Doe Sr.'
        >>> first_name, last_name = split_name(name)
        >>> print(first_name, last_name)
        Jane Doe
    """
    if is_empty_name(full_name):
        return ('', '')

    suffix = ['Jr.', 'Sr.', 'II', 'III', 'IV', 'MD', 'DVM', 'DDS', 'PhD']
    # Split the name string into words
    words = full_name.split()

    # Check if the name has a salutation and/or a suffix
    if len(words) >= 3 and words[0].endswith('.'):
        # The name has a salutation. Remove it from the words list
        words.pop(0)

    if len(words) >= 2 and words[-1] in suffix:
        # The name has a suffix. Remove it from the words list
        words.pop(-1)

    # The first and last names are the first and last words respectively
    first_name = words[0]
    last_name = words[-1]

    # If there are more than 2 words, the middle names are everything in between
    if len(words) > 2:
        middle_names = ' '.join(words[1:-1])
        first_name += ' ' + middle_names

    # Return the first and last names as a tuple
    return (first_name, last_name)


def is_valid_date(date_string: str) -> bool:
    """
    Checks if a date string is in YYYYMMDD format.

    Args:
        date_string: A string representing the date to check, in the format YYYYMMDD.

    Returns:
        True if the date string is in YYYYMMDD format, False otherwise.
    """
    if date_string is None:
        return False
    try:
        datetime.strptime(date_string, '%Y%m%d')
        return True
    except ValueError:
        return False


def get_hashed_date(date_string: str) -> str:
    """
    This function takes a string object of a date in YYYYMMDD
    and returns the first 5 digits of the SHA256 hash of the date.

    Args:
    - date_string (str): a date string in the format YYYYMMDD

    Returns:
    - str: the first 5 digits of the SHA256 hash of the date
    """
    # Check if the date string is in a valid format
    if not is_valid_date(date_string):
        raise ValueError

    # Convert the date string to bytes
    date_bytes = date_string.encode('utf-8')

    # Calculate the SHA256 hash of the date
    sha256_hash = hashlib.sha256(date_bytes)

    # Get the hex digest of the hash and extract the first 5 digits
    hashed_date = sha256_hash.hexdigest()[:5]

    return hashed_date
