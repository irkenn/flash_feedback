from app import app
from models import db, User, Feedback

db.drop_all()
db.create_all()

User.query.delete()

u1 = User.register(
    "CharlieP",
    "123!",
    "charliep@aol.com",
    "Charlie",
    "Peanuts"
)

u2 = User.register(
    "Renee",
    "123",
    "renee@aol.com",
    "Renee",
    "Kermit"
)

db.session.add_all([u1, u2])
db.session.commit()

########## FEEDBACK SECTION ###########

f1 = Feedback.add(
    "First Post",
    "This is my first post and it is so great!",
    "Renee"
)

f2 = Feedback.add(
    "Second Post",
    "This is my second post and it is so great!",
    "CharlieP"
)

db.session.add_all([f1,f2])
db.session.commit()

