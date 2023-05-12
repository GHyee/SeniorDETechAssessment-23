import unittest
from datetime import datetime
from dags.utils import (has_correct_digits,
                        identify_date_format,
                        format_date_of_birth,
                        is_above_age,
                        is_valid_email,
                        is_empty_name,
                        split_name,
                        get_hashed_date
                        )


class TestHasCorrectDigits(unittest.TestCase):
    def test_has_correct_digits_with_eight_digits(self):
        # Test with a mobile number containing 8 digits
        mobile_number = 12345678
        self.assertTrue(has_correct_digits(mobile_number))

    def test_has_correct_digits_with_ten_digits(self):
        # Test with a mobile number containing 10 digits
        mobile_number = 1234567890
        self.assertFalse(has_correct_digits(mobile_number))

    def test_has_correct_digits_with_custom_digits(self):
        # Test with a custom number of digits
        mobile_number = 1234567
        self.assertFalse(has_correct_digits(mobile_number, num_digits=8))


class TestIdentifyDateFormat(unittest.TestCase):
    def test_valid_date_format(self):
        # Test valid date formats
        assert identify_date_format("2022-05-11") == "%Y-%m-%d"
        assert identify_date_format("11-05-2022") == "%d-%m-%Y"
        assert identify_date_format("2022/05/11") == "%Y/%m/%d"
        assert identify_date_format("11/05/2022") == "%d/%m/%Y"
        assert identify_date_format("20220511") == "%Y%m%d"
        assert identify_date_format("11052022") == "%d%m%Y"

    def test_invalid_date_format(self):
        # Test invalid date formats
        assert identify_date_format("2022/05/11 10:00:00") is None
        assert identify_date_format("202205") is None
        assert identify_date_format("May 11, 2022") is None


class TestFormatDateOfBirth(unittest.TestCase):
    def test_format_date_of_birth_default_format(self):
        # Test valid date string in default format
        dob_str = "19900131"
        dob_format = "%Y%m%d"
        expected_output = datetime.strptime(dob_str, "%Y%m%d").strftime("%Y%m%d")
        self.assertEqual(format_date_of_birth(dob_str, dob_format), expected_output)

    def test_format_date_of_birth_non_default_format(self):
        # Test valid date string in non-default format
        dob_str = "31-01-1990"
        dob_format = "%d-%m-%Y"
        expected_output = datetime.strptime(dob_str, dob_format).strftime("%Y%m%d")
        self.assertEqual(format_date_of_birth(dob_str, dob_format), expected_output)

    def test_format_date_of_birth_invalid_date_string(self):
        # Test invalid date string
        dob_str = "19902131"
        dob_format = "%Y%m%d"
        with self.assertRaises(ValueError):
            format_date_of_birth(dob_str, dob_format)


class TestIsAboveAge(unittest.TestCase):

    def test_above_age(self):
        # Applicant born on Jan 11, 2004 will be 18 as of Jan 11, 2022
        dob = "20040111"
        self.assertTrue(is_above_age(dob, 18, "2022-01-11"))

    def test_below_age(self):
        # Applicant born on Jan 12, 2004 will not be 18 as of Jan 11, 2022
        dob = "20040112"
        self.assertFalse(is_above_age(dob, 18, "2022-01-11"))

    def test_exactly_age(self):
        # Applicant born on Jan 11, 2004 will be exactly 18 as of Jan 11, 2022
        dob = "20040111"
        self.assertTrue(is_above_age(dob, 17, "2022-01-11"))

    def test_invalid_dob(self):
        # Invalid DOB format should raise a ValueError
        dob = "01/11/2004"
        with self.assertRaises(ValueError):
            is_above_age(dob, 18, "2022-01-11")


class TestIsValidEmail(unittest.TestCase):
    def test_valid_email_with_default_suffixes(self):
        self.assertTrue(is_valid_email("john.doe@example.com"))
        self.assertTrue(is_valid_email("jane.doe@example.net"))

    def test_valid_email_with_custom_suffixes(self):
        suffixes = [".org", ".io"]
        self.assertTrue(is_valid_email("john.doe@example.org", suffixes=suffixes))
        self.assertTrue(is_valid_email("jane.doe@example.io", suffixes=suffixes))

    def test_invalid_email(self):
        self.assertFalse(is_valid_email(""))
        self.assertFalse(is_valid_email("john.doe@example"))
        self.assertFalse(is_valid_email("john.doe@example.org", suffixes=[".com", ".net"]))


class TestIsEmptyName(unittest.TestCase):
    def test_empty_name(self):
        # Test empty name
        self.assertTrue(is_empty_name(''))
        self.assertTrue(is_empty_name(None))

    def test_non_empty_name(self):
        # Test non-empty name
        self.assertFalse(is_empty_name('John Doe'))
        self.assertFalse(is_empty_name('  Jane Smith  '))


class TestSplitName(unittest.TestCase):
    def test_salutation_and_suffix(self):
        # Test a name with a salutation and a suffix
        name1 = 'Dr. Jane Doe Sr.'
        first_name1, last_name1 = split_name(name1)
        self.assertEqual(first_name1, 'Jane')
        self.assertEqual(last_name1, 'Doe')

    def test_suffix(self):
        # Test a name with a suffix but no salutation
        name2 = 'John Smith III'
        first_name2, last_name2 = split_name(name2)
        self.assertEqual(first_name2, 'John')
        self.assertEqual(last_name2, 'Smith')

    def test_salutation(self):
        # Test a name with a salutation but no suffix
        name3 = 'Mrs. Emily Brown'
        first_name3, last_name3 = split_name(name3)
        self.assertEqual(first_name3, 'Emily')
        self.assertEqual(last_name3, 'Brown')

    def test_no_salutation_and_suffix(self):
        # Test a name with no salutation or suffix
        name4 = 'David Lee'
        first_name4, last_name4 = split_name(name4)
        self.assertEqual(first_name4, 'David')
        self.assertEqual(last_name4, 'Lee')


class TestGetHashedDate(unittest.TestCase):
    def test_get_hashed_date(self):
        # Test with date 1 Jan 2022
        date_input = '20220101'
        expected_result = "23024"
        self.assertEqual(get_hashed_date(date_input), expected_result)

        # Test with date 31 Dec 2021
        date_input = '20211231'
        expected_result = "66078"
        self.assertEqual(get_hashed_date(date_input), expected_result)

        # Test with date 15 Sep 2023
        date_input = '20230915'
        expected_result = "a1a80"
        self.assertEqual(get_hashed_date(date_input), expected_result)

    def test_get_hashed_date_invalid_input(self):
        # Test with invalid input type
        date_input = "2022-12-25"
        with self.assertRaises(ValueError):
            get_hashed_date(date_input)

        # Test with None input
        date_input = None
        with self.assertRaises(ValueError):
            get_hashed_date(date_input)
