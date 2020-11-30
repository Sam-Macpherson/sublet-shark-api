import datetime

from model_bakery.recipe import Recipe


ListingRecipe = Recipe(
    'listings.Listing',
    address='132 Marshall Street',
    accommodation_type=1,
    start_date=datetime.date(2050, 1, 1),
    end_date=datetime.date(2050, 4, 30),
)
