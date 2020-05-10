import sqlite3
import random

marks = ['Audi', 'BMW', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Lada (ВАЗ)', 'Mazda', 'Mercedes-Benz', 'Mitsubishi',
         'Nissan', 'Renault', 'Skoda', 'Toyota', 'Volkswagen', 'Acura', 'Daihatsu', 'Datsun', 'Honda', 'Infiniti',
         'Isuzu', 'Lexus', 'Mazda', 'Mitsubishi', 'Nissan', 'Scion', 'Subaru', 'Suzuki', 'Toyota', 'Buick', 'Cadillac',
         'Chevrolet', 'Chrysler', 'Dodge', 'Ford', 'GMC', 'Hummer', 'Jeep', 'Lincoln', 'Mercury', 'Oldsmobile',
         'Pontiac', 'Tesla', 'Aurus', 'Lada (ВАЗ)', 'ГАЗ', 'Москвич', 'ТагАЗ', 'УАЗ', 'Audi', 'BMW', 'Mercedes-Benz',
         'Opel', 'Porsche', 'Volkswagen', 'Daewoo', 'Genesis', 'Hyundai', 'Kia', 'SsangYong', 'Alfa Romeo',
         'Aston Martin', 'Bentley', 'Bugatti', 'Citroen', 'DS', 'Ferrari', 'Fiat', 'Jaguar', 'Lamborghini', 'Lancia',
         'Land Rover', 'Maserati', 'Maybach', 'Mini', 'Peugeot', 'Ravon', 'Renault', 'Rolls-Royce', 'Rover', 'Saab',
         'SEAT', 'Skoda', 'Smart', 'Volvo', 'ZAZ', 'Brilliance', 'BYD', 'Changan', 'Chery', 'DongFeng', 'FAW', 'Foton',
         'GAC', 'Geely', 'Great Wall', 'Haima', 'Haval', 'JAC', 'Lifan', 'Luxgen', 'Zotye']

colors = ['White', 'Yellow', 'Blue', 'Red', 'Green', 'Black', 'Brown', 'Azure', 'Ivory', 'Teal', 'Silver', 'Purple',
          'Navy blue', 'Pea green', 'Gray', 'Orange', 'Maroon', 'Charcoal', 'Aquamarine', 'Coral', 'Fuchsia', 'Wheat',
          'Lime', 'Crimson', 'Khaki', 'Hot pink', 'Magenta', 'Olden', 'Plum', 'Olive', 'Cyan']


def create(table_name, fields):
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE " + table_name + "(" + (','.join([' '.join(field) for field in fields])) + ")"
    )
    db.commit()
    db.close()


def insert(table_name, fields, data):
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    cur.executemany(
        "INSERT INTO " + table_name + "(" + (','.join(fields)) + ") VALUES (" + (','.join(['?'] * len(data[0]))) + ")",
        data)
    db.commit()
    db.close()


def get(table_name):
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    cur.execute("SELECT * FROM " + table_name)
    result = cur.fetchall()
    db.close()
    return result


def delete(table_name, field, value):
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    cur.execute("DELETE FROM `" + table_name + "` WHERE `" + field + "`=?", (value,))
    db.commit()
    db.close()


# create('cars',
#        [('id', 'integer PRIMARY KEY AUTOINCREMENT'), ('mark', 'text'), ('color', 'text'), ('number', 'integer')])

# insert('cars', ['mark', 'color', 'number'], [
#     (random.choice(marks), random.choice(colors), random.randint(1000, 9999)),
#     (random.choice(marks), random.choice(colors), random.randint(1000, 9999)),
#     (random.choice(marks), random.choice(colors), random.randint(1000, 9999)),
# ])
#
# delete('cars', 'number', 6451)
# print(get('cars'))

create('groups', [('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), ('groupName', 'TEXT')])
create('user', [('id', 'INTEGER'), ('groupId', 'INTEGER'),
                ('FOREIGN KEY("groupId")', 'REFERENCES "groups"("id")')])
