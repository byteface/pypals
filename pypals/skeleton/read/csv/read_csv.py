def run(o):    
    print("ok mike, i will read the csv")

    import csv
    import time
    
    def load_data(csv_fname):
        with open(csv_fname, "r", encoding="latin-1") as records:
            for row in csv.reader(records):
                yield row

    rows = iter(load_data(o.context.COMMAND_PATH + "/" + 'some.csv'))
    print(next(rows)) # skips the column names

    some_data=[]
    for row in rows:
        try:
            print(row[0])
            some_data.append(row[0])
        except Exception as e:
            print('failed on row...')
            print(e)

    print('ALL RECORDS WERE CHECKED')
    o.memory.create( o.context, some_data, 'output.json' )
