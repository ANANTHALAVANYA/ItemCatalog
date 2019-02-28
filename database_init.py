from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

engine = create_engine('sqlite:///pendrives.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
session = DBSession()

# Delete BykesCompanyName if exisitng.
session.query(PenDrivesCompanyName).delete()
# Delete PenDriveName if exisitng.
session.query(PenDriveName).delete()
# Delete PenDriveUser if exisitng.
session.query(PenDriveUser).delete()

# Create sample users data
User1 = PenDriveUser(name="ANANTHA LAVANYA TUMMALAPALLI",
                 email="lavanyatummala777@gmail.com",
                 picture='sample.jpg')
session.add(User1)
session.commit()
print ("Successfully Add First User")
User1 = PenDriveUser(name="KANAMARLAPUDI TEJASRI",
                 email="ammulukruthika777@gmail.com",
                 picture='sample.jpg')
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample byke companys
Company1 = PenDrivesCompanyName(name="SANDISK",
                     user_id=1)
session.add(Company1)
session.commit()

Company2 = PenDrivesCompanyName(name="KINGSTON",
                     user_id=1)
session.add(Company2)
session.commit

Company3 = PenDrivesCompanyName(name="STRONTIUM",
                     user_id=1)
session.add(Company3)
session.commit()

Company4 = PenDrivesCompanyName(name="SONY",
                     user_id=1)
session.add(Company4)
session.commit()

Company5 = PenDrivesCompanyName(name="HP",
                     user_id=1)
session.add(Company5)
session.commit()

Company6 = PenDrivesCompanyName(name="SOLIMO",
                     user_id=1)
session.add(Company6)
session.commit()

# Populare a bykes with models for testing
# Using different users for bykes names year also
pendriveName1 = PenDriveName(name="Cruzer Blade",
                       drives_number="1",
                       item_capacity="32GB",
                       drive_name="USB2.0",
                       item_color="Multicolor",
                       transferspeed="480 megabits per second",
                       item_cost="427RS",
                       otgfacility="no",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=1,
                       user_id=1)
session.add(pendriveName1)
session.commit()
pendriveName10 = PenDriveName(name="Ultra Dual Drive",
                       drives_number="2",
                       item_capacity="128GB",
                       drive_name="USB3.0",
                       item_color="Silver",
                       transferspeed="640 megabits per second",
                       item_cost="2370RS",
                       otgfacility="yes",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=1,
                       user_id=1)
session.add(pendriveName10)
session.commit()
pendriveName100 = PenDriveName(name="Ultra Dual Drive",
                       drives_number="2",
                       item_capacity="32GB",
                       drive_name="USB3.0",
                       item_color="Gold",
                       transferspeed="640 megabits per second",
                       item_cost="589RS",
                       otgfacility="yes",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=1,
                       user_id=1)
session.add(pendriveName100)
session.commit()
pendriveName2 = PenDriveName(name="DTIG",
                       drives_number="1",
                       item_capacity="32GB",
                       drive_name="USB3.0",
                       item_color="White and red",
                       transferspeed="640 megabits per second",
                       item_cost="499RS",
                       otgfacility="no",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=2,
                       user_id=1)
session.add(pendriveName2)
session.commit()
pendriveName20 = PenDriveName(name="DTIG4",
                       drives_number="2",
                       item_capacity="64GB",
                       drive_name="USB3.0",
                       item_color="Gold",
                       transferspeed="640 megabits per second",
                       item_cost="2333RS",
                       otgfacility="yes",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=2,
                       user_id=1)
session.add(pendriveName20)
session.commit()
pendriveName200 = PenDriveName(name="Data Traveler",
                       drives_number="2",
                       item_capacity="32GB",
                       drive_name="USB2.0",
                       item_color="Silver",
                       transferspeed="480 megabits per second",
                       item_cost="569RS",
                       otgfacility="no",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=2,
                       user_id=1)
session.add(pendriveName200)
session.commit()
pendriveName2000 = PenDriveName(name="Data Traveler",
                       drives_number="1",
                       item_capacity="16GB",
                       drive_name="USB2.0",
                       item_color="Black",
                       transferspeed="480 megabits per second",
                       item_cost="522RS",
                       otgfacility="yes",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=2,
                       user_id=1)
session.add(pendriveName2000)
session.commit()
pendriveName3 = PenDriveName(name="Ammo",
                       drives_number="1",
                       item_capacity="8GB",
                       drive_name="USB2.0",
                       item_color="Silver",
                       transferspeed="480 megabits per second",
                       item_cost="567RS",
                       otgfacility="no",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=3,
                       user_id=1)
session.add(pendriveName3)
session.commit()
pendriveName30 = PenDriveName(name="Nitro Plus",
                       drives_number="2",
                       item_capacity="32GB",
                       drive_name="USB2.0",
                       item_color="silver",
                       transferspeed="480 megabits per second",
                       item_cost="999RS",
                       otgfacility="yes",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=3,
                       user_id=1)
session.add(pendriveName30)
session.commit()
pendriveName300 = PenDriveName(name="pollex",
                       drives_number="1",
                       item_capacity="32GB",
                       drive_name="USB2.0",
                       item_color="black",
                       transferspeed="480 megabits per second",
                       item_cost="369RS",
                       otgfacility="no",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=3,
                       user_id=1)
session.add(pendriveName300)
session.commit()
pendriveName4 = PenDriveName(name="Microvault",
                       drives_number="1",
                       item_capacity="16GB",
                       drive_name="USB2.0",
                       item_color="white",
                       transferspeed="480 megabits per second",
                       item_cost="340RS",
                       otgfacility="no",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=4,
                       user_id=1)
session.add(pendriveName4)
session.commit()
pendriveName40 = PenDriveName(name="USM",
                       drives_number="1",
                       item_capacity="32GB",
                       drive_name="USB2.0",
                       item_color="Gold",
                       transferspeed="480 megabits per second",
                       item_cost="410RS",
                       otgfacility="no",
                       warranty="5 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=4,
                       user_id=1)
session.add(pendriveName40)
session.commit()
pendriveName400 = PenDriveName(name="",
                       drives_number="2",
                       item_capacity="64GB",
                       drive_name="USB3.1",
                       item_color="yellow",
                       transferspeed="10 gigabits per second",
                       item_cost="979RS",
                       otgfacility="yes",
                       warranty="2 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=4,
                       user_id=1)
session.add(pendriveName400)
session.commit()
pendriveName5 = PenDriveName(name="v152w",
                       drives_number="1",
                       item_capacity="32GB",
                       drive_name="USB2.0",
                       item_color="Blue",
                       transferspeed="480 megabits per second",
                       item_cost="499RS",
                       otgfacility="no",
                       warranty="1 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=5,
                       user_id=1)
session.add(pendriveName100)
session.commit()
pendriveName50 = PenDriveName(name="x765w",
                       drives_number="1",
                       item_capacity="32GB",
                       drive_name="USB3.0",
                       item_color="white",
                       transferspeed="640 megabits per second",
                       item_cost="694RS",
                       otgfacility="yes",
                       warranty="2 years",
                       date=datetime.datetime.now(),
                       pendrivecompanyid=5,
                       user_id=1)
session.add(pendriveName50)
session.commit()

print("Your Pendrives database has been inserted!")
