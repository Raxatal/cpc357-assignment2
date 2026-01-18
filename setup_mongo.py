import pymongo
from pymongo.errors import OperationFailure

# MongoDB connection (no auth initially)
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Step 1: Create admin user in admin database
try:
    admin_db = client["admin"]
    admin_db.command("createUser", "admin",
                     pwd="admin123",
                     roles=[{"role": "userAdminAnyDatabase", "db": "admin"}])
    print("Admin user created successfully.")
except OperationFailure as e:
    if "already exists" in str(e):
        print("Admin user already exists. Skipping creation.")
    else:
        print("Error creating admin user:", e)

# Step 2: Create monitor user in library_monitor database
try:
    lm_db = client["library_monitor"]
    lm_db.command("createUser", "monitor",
                  pwd="Password123",
                  roles=[{"role": "readWrite", "db": "library_monitor"}])
    print("Monitor user created successfully.")
except OperationFailure as e:
    if "already exists" in str(e):
        print("Monitor user already exists. Skipping creation.")
    else:
        print("Error creating monitor user:", e)
