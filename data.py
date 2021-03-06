from faker import Faker
from flask_app import User

# Creating an instance of a Faker object
fake = Faker()

Creating and inserting 100 email addresses and registration dates generated by fake into the database
for _ in range(100):
    User.add_user(email = fake.email(), created_at = fake.past_datetime(start_date='-365d'))
