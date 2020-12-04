import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from model_bakery import baker
from rest_framework import status

from base.tests import TestHelpers, SubletSharkAPITestCase
from listings.models.listing import AccommodationType
from listings.models.room import BedType


class ListingTestCase(TestCase):
    """Tests for the Listings model."""

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


class ListingsViewSetTestCase(SubletSharkAPITestCase):
    """Tests for the listings view set."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = cls.make_user()

    def setUp(self):
        super().setUp()
        self.url = reverse('listings:listings-list')
        self.client.force_authenticate(user=self.user)
        self.first_listing = baker.make_recipe(
            'listings.ListingRecipe',
            start_date=datetime.date(2019, 12, 31),
            end_date=datetime.date(2020, 4, 29),
        )
        self.second_listing = baker.make_recipe(
            'listings.ListingRecipe',
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2020, 4, 30),
            accommodation_type=AccommodationType.APARTMENT,
        )
        self.rooms = [
            baker.make_recipe(
                'listings.RoomRecipe',
                listing=self.second_listing
            )
            for _ in range(5)
        ]

    def test_start_date_filter(self):
        """Test that listings before start_date are not returned, and listings
        after start_date are.
        """
        response = self.client.get(
            self.add_query_params(self.url, start_date='2020-01-01')
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure only the second listing was returned.
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['id'], str(self.second_listing.id))

    def test_end_date_filter(self):
        """Test that the listings that end after end_date are not returned,
        and listings that end before end_date are.
        """
        response = self.client.get(
            self.add_query_params(self.url, end_date='2020-04-29')
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure only the first listing was returned.
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['id'], str(self.first_listing.id))

    def test_ensuite_filter(self):
        """Test that the listings whose rooms that match the query are
        returned.
        """
        # Case 1: None of the rooms for the listing have an ensuite, should
        # return 0 listings.
        response = self.client.get(
            self.add_query_params(self.url, ensuite=True)
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 0)
        # Case 2: Any number of the rooms for a listing have an ensuite, should
        # return those listings.
        self.rooms[0].ensuite = True
        self.rooms[0].save()
        response = self.client.get(
            self.add_query_params(self.url, ensuite=True)
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 1)

    def test_minifridge_filter(self):
        """Test that the listings which have rooms that match the query are
        returned.
        """
        # Case 1: None of the rooms for the listing have a minifridge, should
        # return 0 listings.
        response = self.client.get(
            self.add_query_params(self.url, minifridge=True)
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 0)
        # Case 2: Any number of the rooms for a listing have an ensuite, should
        # return those listings.
        self.rooms[3].minifridge = True
        self.rooms[3].save()
        response = self.client.get(
            self.add_query_params(self.url, minifridge=True)
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 1)

    def test_bed_type_filter(self):
        """Test that the listings which have any rooms that match the bed
        type query are returned.
        """
        # Case 1: None of the rooms for the listing have a king bed, should
        # return 0 listings.
        response = self.client.get(
            self.add_query_params(self.url, bed_type=f'{BedType.KING}')
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 0)
        # Case 2: All of the rooms have single beds, should return 1 listing.
        response = self.client.get(
            self.add_query_params(self.url, bed_type=f'{BedType.SINGLE}')
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 1)
        # Case 3: Combination of bed types should return 1 listing if any of
        # them are valid.
        self.rooms[0].bed_type = BedType.DOUBLE
        self.rooms[0].save()
        self.rooms[1].bed_type = BedType.QUEEN
        self.rooms[1].save()
        response = self.client.get(
            self.add_query_params(self.url, bed_type=f'{BedType.DOUBLE}')
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 1)
        response = self.client.get(
            self.add_query_params(self.url, bed_type=f'{BedType.KING},'
                                                     f'{BedType.DOUBLE}')
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 1)
