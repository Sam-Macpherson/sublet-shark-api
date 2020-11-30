import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from model_bakery import baker


class ListingTestCase(TestCase):

    def setUp(self):
        self.listing = baker.make_recipe('listings.ListingRecipe')

    def test_term_length_one_month(self):
        """Test that all the combinations of distances between start and end
        date that should be displayed as 1 month are correct.
        """
        date_pairs = [
            # January 1 - January 31
            (datetime.date(2020, 1, 1), datetime.date(2020, 1, 31)),
            # January 1 - February 1
            (datetime.date(2020, 1, 1), datetime.date(2020, 2, 1)),
            # February 1 - February 28
            (datetime.date(2020, 2, 1), datetime.date(2020, 2, 28)),
            # September 1 - September 30
            (datetime.date(2020, 9, 1), datetime.date(2020, 9, 30)),
            # January 15 - February 28
            (datetime.date(2020, 1, 15), datetime.date(2020, 2, 28)),
            # January 30 - March 1
            (datetime.date(2020, 1, 30), datetime.date(2020, 3, 1)),
            # May 15 - June 6, 1 month
            (datetime.date(2020, 5, 15), datetime.date(2020, 6, 6)),
            # January 1 - February 15
            (datetime.date(2020, 1, 1), datetime.date(2020, 2, 15)),
        ]
        for start_date, end_date in date_pairs:
            self.listing.start_date = start_date
            self.listing.end_date = end_date
            self.listing.save(update_fields=['start_date', 'end_date'])
            self.assertEqual(self.listing.term_length, 1)

    def test_term_length_greater_than_one_month(self):
        """Test to ensure that term lengths that span multiple months are
        calculated correctly.
        """
        # A tuple in date_data is of the form: (start_date, end_date, # months)
        date_data = [
            # January 1 - February 28, 2 months
            (datetime.date(2020, 1, 1), datetime.date(2020, 2, 28), 2),
            # January 1 - February 27, 2 months
            (datetime.date(2020, 1, 1), datetime.date(2020, 2, 27), 2),
            # January 1 - February 21, 2 months
            (datetime.date(2020, 1, 1), datetime.date(2020, 2, 21), 2),
            # January 1 - March 1, 2 months
            (datetime.date(2020, 1, 1), datetime.date(2020, 3, 1), 2),
            # January 15 - March 14, 2 months
            (datetime.date(2020, 1, 15), datetime.date(2020, 3, 14), 2),
            # January 1 - August 30, 8 months
            (datetime.date(2020, 1, 1), datetime.date(2020, 8, 30), 8),
            # January 1 - August 1, 7 months
            (datetime.date(2020, 1, 1), datetime.date(2020, 8, 1), 7),
        ]
        for start_date, end_date, months in date_data:
            self.listing.start_date = start_date
            self.listing.end_date = end_date
            self.listing.save(update_fields=['start_date', 'end_date'])
            self.assertEqual(self.listing.term_length, months)

    def test_bad_date_combinations(self):
        """Ensure that bad date combinations cannot be saved to the database."""
        with self.assertRaises(ValidationError):
            # Start date must be after end date.
            self.listing.start_date = datetime.date(2020, 1, 2)
            self.listing.end_date = datetime.date(2020, 1, 1)
            self.listing.save(update_fields=['start_date', 'end_date'])
        with self.assertRaises(ValidationError):
            # Less than 1 month cannot be saved.
            self.listing.start_date = datetime.date(2020, 1, 1)
            self.listing.end_date = datetime.date(2020, 1, 15)
            self.listing.save(update_fields=['start_date', 'end_date'])
