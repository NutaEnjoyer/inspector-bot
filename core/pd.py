from os import path
from utils.pd import PandasDatabase
from utils.table import User, Word, GroupMessage, City


pd = PandasDatabase(
    filename=path.join("data/database.txt"),
    tables=dict(user=User, word=Word, gmsg=GroupMessage, city=City)
)

