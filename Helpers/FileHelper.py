import json
from Singleton import *
import csv
import pandas


class FileHelper(metaclass=Singleton):
    def write_log(self, txt, path="Data/log.txt"):
        with open(path, 'a') as file:
            file.write(txt+"\n")

    def read_csv_dict(self, path="Data/orders.csv"):
        return pandas.read_csv(path, index_col=False)

    def update_line(self, headers, key, value, path="Data/orders.csv"):
        with open(path, "w") as file:
            reader = csv.DictReader(file, fieldnames=headers)
            writer = csv.DictWriter(file, fieldnames=headers)
            for row in reader:
                if key == row[key]:
                    row[key] = value
                # write the row either way
                writer.writerow(row)

    def write_csv_line(self, df, path="Data/orders.csv"):
        return df.to_csv(path, encoding='utf-8', index=False)
