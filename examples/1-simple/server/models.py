from datetime import datetime

user_storage = []  # Mimics a simple database.


def get_free_user_id():
    """Utility function to retrieve the lowest ID without a user."""
    id_to_check = 1
    user = User.from_id(id_to_check)
    while user is not None:
        id_to_check += 1
        user = User.from_id(id_to_check)
    return id_to_check


class User:
    """User class."""

    def __init__(self, id, first_name, last_name, password, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.register_date = datetime.now()

    @classmethod
    def from_id(cls, user_id):
        """Searches for a user in the database, using it's ID.

        If no user exists with this ID, return None.
        """
        return next((user for user in user_storage if user.id == int(user_id)), None)

    def save(self):
        """Saves the user in the database."""
        user = self.from_id(self.id)
        if user is not None:  # User already saved in the database, nothing to do
            return

        user_storage.append(self)
