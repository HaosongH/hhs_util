import csv

def initialize_csv(file, mode = "w"):
    csv_f = open(file, mode, encoding = "utf-8", newline = "")
    csv_writer = csv.writer(csv_f)
    return csv_f, csv_writer

def close_csv(f):
    f.close()