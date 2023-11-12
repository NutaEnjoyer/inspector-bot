from warnings import simplefilter
from typing import Any, Dict
from os import path
from ast import literal_eval

from pydantic import BaseModel
from pandas import DataFrame

from .exception import NonExistTable



class PandasDatabase:


    def __init__(self, filename : str, tables : Dict[str, BaseModel]) -> None:
        """
        ! Word
        """
        
        simplefilter(action='ignore', category=FutureWarning)

        self._filename = filename

        self.local = dict()

        for key, value in tables.items():
            self.local.setdefault(key, DataFrame(
                columns=[key for key in value.model_fields.keys() if key != "index"], 
            ))

        if path.exists(filename):
            self._read()


    def insert(self, tablename : str, value : BaseModel) -> None:
        table = self.get_table(tablename)
        
        if table is None: 
            raise NonExistTable
    
        table.loc[value.index] = value.model_dump(exclude=["index"]) 
        
        self._write()


    def get_table(self, tablename : str) -> DataFrame:
        
        try:
            return self.local.get(tablename)
        except KeyError:
            return DataFrame()


    def update_value(self, tablename : str, index : Any, column : Any, value : Any) -> None:

        table = self.local.get(tablename)
        try:
            table.at[index, column] = value
            self._write()
        except KeyError:
            print("Key err at update_value")

    def inplace_index(self, tablename : str, lastindex : Any, newindex : Any) -> None:
        
        table = self.get_table(tablename)
        
        table.rename(index={lastindex : newindex}, inplace=True)

        self._write()
        

    def inplace_value(self, tablename : str, index : str, column : str, value : Any) -> None:
        
        self.local[tablename].at[index, column] = value
        self._write()


    def _write(self) -> None:
        """
        Save all data to json
        """
        
        valid_data = dict()

        for name, df in self.local.items():
            valid_data.setdefault(name, df.to_dict())

        with open(self._filename, "w") as file:
            file.write(str(valid_data))


    def _read(self) -> None:
        """
        Save all data to local var
        """

        with open(self._filename, "r") as file:
            data = literal_eval(file.read())

        for key, value in data.items():
            self.local[key] = DataFrame(data=value, dtype=object)

    
