import mysql.connector




# Connect to MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",       # Replace with your MySQL username
    password="krishnavamsy@0411"     # Replace with your MySQL password
)

cursor = db.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS MilitaryDB")
cursor.execute("USE MilitaryDB")

# Define each table as per the ER diagram
tables = {}

tables['WAR'] = '''
    CREATE TABLE IF NOT EXISTS WAR (
        War_no INTEGER PRIMARY KEY,
        Status VARCHAR(20),
        Pincode INTEGER,
        Date DATE
    )
'''

tables['Ranks'] = '''
    CREATE TABLE IF NOT EXISTS Ranks (
        Rank_name VARCHAR(30) PRIMARY KEY,
        Rank_ID INT
    )
'''

tables['Camps'] = '''
    CREATE TABLE IF NOT EXISTS Camps (
        Camp_name VARCHAR(20) PRIMARY KEY,
        camp_strength INTEGER
    )
'''


tables['Squad'] = '''
    CREATE TABLE IF NOT EXISTS Squad (
        Squad_id INTEGER PRIMARY KEY,
        No_of_soldiers INTEGER,
        Camp VARCHAR(20),
        Year YEAR,
        FOREIGN KEY (Camp) REFERENCES Camps(Camp_name)
    )
'''

tables['Vehicles'] = '''
    CREATE TABLE IF NOT EXISTS Vehicles (
        V_ID INTEGER PRIMARY KEY,
        V_name VARCHAR(50),
        V_model VARCHAR(100)
    )
'''

tables['Vehicles_assigned'] = '''
    CREATE TABLE IF NOT EXISTS Vehicles_assigned (
        V_ID INTEGER PRIMARY KEY,
        V_name VARCHAR(20),
        Squad_ID INTEGER,
        FOREIGN KEY (V_ID) REFERENCES  Vehicles(V_ID),
        FOREIGN KEY (Squad_ID) REFERENCES Squad(Squad_ID)
     )
'''

tables['Divisions'] = '''
    CREATE TABLE IF NOT EXISTS Divisions (
        Div_name VARCHAR(50) PRIMARY KEY,
        Div_ID INTEGER
    )
'''

tables['SOLDIERS'] = '''
    CREATE TABLE IF NOT EXISTS SOLDIERS (
        ID INTEGER PRIMARY KEY,
        Name VARCHAR(30),
        DOB DATE,
        DOJ DATE,
        Gender VARCHAR(10),
        Height FLOAT,
        Weight FLOAT,
        Division VARCHAR(30),
        Maritial_status VARCHAR(10),
        Blood_type VARCHAR(3),
        Phone_no VARCHAR(10),
        Ranks VARCHAR(30),
        Camp Varchar(20),
        Squad_ID INTEGER,
        FOREIGN KEY (Ranks) REFERENCES Ranks(Rank_name),
        FOREIGN KEY (Camp) REFERENCES Camps(Camp_name),
        FOREIGN KEY (Squad_ID) REFERENCES Squad(Squad_id),
        FOREIGN KEY (Division) REFERENCES Divisions(Div_name)
    )
'''

tables['Soldier_status'] = '''
    CREATE TABLE IF NOT EXISTS Soldier_status (
        ID INTEGER PRIMARY KEY,
        Survived VARCHAR(20),
        War_ID INTEGER,
        FOREIGN KEY (War_ID) REFERENCES WAR(War_no),
        FOREIGN KEY (ID) REFERENCES SOLDIERS(ID)
    )
'''

tables['Training_Details'] = '''
    CREATE TABLE IF NOT EXISTS Training_Details (
        ID INTEGER PRIMARY KEY,
        Fitness_score FLOAT,
        Shooting_accuracy FLOAT,
        Sprint_speed_100m FLOAT,
        FOREIGN KEY (ID) REFERENCES SOLDIERS(ID)
    )
'''

tables['Leaves_taken'] = '''
    CREATE TABLE IF NOT EXISTS Leaves_taken (
        ID INTEGER PRIMARY KEY,
        No_of_leaves INTEGER,
        Reason VARCHAR(100),
        FOREIGN KEY (ID) REFERENCES SOLDIERS(ID)
    )
'''
tables['WEAPON_CATEGORY'] = '''
    CREATE TABLE IF NOT EXISTS WEAPON_CATEGORY (
        Category_no INTEGER PRIMARY KEY,
        Category VARCHAR(20)
    )
'''

tables['Weapon_Catalogue'] = '''
    CREATE TABLE IF NOT EXISTS Weapon_Catalogue (
        Weapon_ID INTEGER PRIMARY KEY,
        Weapon_name VARCHAR(20),
        Category_no INTEGER,
        FOREIGN KEY (Category_no) REFERENCES WEAPON_CATEGORY(Category_no)
    )
'''

tables['Weapon_Assigned'] = '''
    CREATE TABLE IF NOT EXISTS Weapon_Assigned (
        ID INTEGER PRIMARY KEY,
        Weapon_ID INTEGER,
        Date DATE,
        FOREIGN KEY (ID) REFERENCES SOLDIERS(ID),
        FOREIGN KEY (Weapon_ID) REFERENCES Weapon_Catalogue(Weapon_ID)
    )
'''


tables['Achievements'] = '''
    CREATE TABLE IF NOT EXISTS Achievements (
        ID INTEGER PRIMARY KEY,
        Medal VARCHAR(20),
        Date_of_receiving DATE,
        FOREIGN KEY (ID) REFERENCES SOLDIERS(ID)
    )
'''

tables['Login'] = '''
    CREATE TABLE IF NOT EXISTS Login (
        ID INTEGER PRIMARY KEY,
        Username VARCHAR(50),
        Password VARCHAR(20),
        FOREIGN KEY (ID) REFERENCES SOLDIERS(ID)
    )
'''

tables['Promotion'] = '''
    CREATE TABLE IF NOT EXISTS Promotion (
        Promotion_ID INTEGER PRIMARY KEY,
        Soldier_ID INTEGER,
        New_rank VARCHAR(20),
        Promotion_Date DATE,
        FOREIGN KEY (Soldier_ID) REFERENCES SOLDIERS(ID)
    )
'''


tables['Address'] = '''
    CREATE TABLE IF NOT EXISTS Address (
        ID INTEGER PRIMARY KEY,
        Pincode INTEGER,
        District VARCHAR(80),
        City VARCHAR(20),
        STATE VARCHAR(20),
        Home_phone_no VARCHAR(10),
        Address_line VARCHAR(500),
        FOREIGN KEY (ID) REFERENCES SOLDIERS(ID)
    )
'''

tables['Captains'] = '''
    CREATE TABLE IF NOT EXISTS Captains (
        Captain_ID INTEGER PRIMARY KEY,
        Captain_name VARCHAR(20),
        Squad_ID INTEGER,
        Camp VARCHAR(20),
        FOREIGN KEY (Squad_ID) REFERENCES Squad(Squad_ID),
        FOREIGN KEY (Camp) REFERENCES Camps(Camp_name)
    )
'''



# Create tables
for table_name, table_sql in tables.items():
    cursor.execute(table_sql)
    print(f"Table {table_name} created successfully.")


cursor.execute("""select rank_name from Ranks""")
if len(cursor.fetchall())==0:
    # Adding values to the Ranks and Divisions tables
    cursor.execute("""
    INSERT INTO Ranks (rank_name, rank_id) VALUES
    ('Field Marshal', 1),
    ('General', 2),
    ('Lieutenant General', 3),
    ('Major General', 4),
    ('Brigadier General', 5),
    ('Colonel', 6),
    ('Lieutenant Colonel', 7),
    ('Major', 8),
    ('Captain', 9),
    ('Lieutenant', 10),
    ('Sergeant Major', 11),
    ('Sergeant', 12),
    ('Corporal', 13),
    ('Private', 14)
    """)  # Closing parenthesis for multi-row insert


cursor.execute("""select div_id from divisions""")
if len(cursor.fetchall())==0:
    cursor.execute("""
    INSERT INTO Divisions (div_name, div_id) VALUES
    ('Infantry', 1),
    ('Armored', 2),
    ('Mechanized', 3),
    ('Airborne', 4),
    ('Mountain', 5)
    """)  # Closing parenthesis for multi-row insert



#add default admin

cursor.execute("""select * from Login where ID=0 and Username='General@1' """)
if len(cursor.fetchall())==0:
    cursor.execute("INSERT INTO camps values('Admin',1)")
    cursor.execute("INSERT INTO squad values(0,0,'Admin','2000')")
    cursor.execute("""INSERT INTO  soldiers values (0,'Default','1999-1-1','1999-1-1','Male','150','50','Infantry','Unmarried','A','8106334572','General','Admin',0)""")
    cursor.execute("""INSERT INTO Login (ID,Username, Password)
                      values ('0', 'General@1','military');
                   """)

# Commit the transaction to save the inserted data
db.commit()


# Close connection
cursor.close()
db.close()
