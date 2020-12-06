import datetime

from model_bakery.recipe import Recipe, foreign_key

from listings.models.listing import AccommodationType

ListingRecipe = Recipe(
    'listings.Listing',
    address='132 Marshall Street, Waterloo, Ontario, N2J4E6',
    accommodation_type=AccommodationType.APARTMENT,
    start_date=datetime.date(2050, 1, 1),
    end_date=datetime.date(2050, 4, 30),
)

RoomRecipe = Recipe(
    'listings.Room',
    listing=foreign_key(ListingRecipe),
)
