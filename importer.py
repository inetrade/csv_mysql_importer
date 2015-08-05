import csv
import mysql.connector


# data format example:
# "2348";"Meyer Hans";;"0049123456567";

source_csv = 'some_file.csv'

# database connection
cnx = mysql.connector.connect(user='root', database='geheim')
cursor = cnx.cursor()

with open(source_csv, newline='') as csvfile:
    csv_data = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in csv_data:
        try:

            # manipulate data
            short_code = row[0]
            name = row[1]
            some_field = row[2]
            phone_number = row[3]

            query = ("""
                        INSERT INTO tablename
                            (short_code, name, some_field, phone_number)
                        VALUES 
                            (%s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE 
                                                -- no need to update the PK
                        name = VALUES(%s), 
                        some_field = VALUES(%s), 
                        phone_number = VALUES(%s) ;
                        """
                        )

            data = (short_code, name, some_field, phone_number,
                    name, some_field, phone_number,)
            cursor.execute(query, data)
            cursor.close()

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            cnx.rollback()

    cnx.commit()
cnx.close()

