from os import path
from utils.pt import PandasDatabase
from utils.table import User, Word, GroupMessage


pd = PandasDatabase(
    filename=path.join("database.pt"),
    tables=dict(user=User, word=Word, gmsg=GroupMessage)
)

