import os
os.environ['MONGO_MOCK'] = "true"
os.environ["MONGO_DB_NAME"] = "pytest"
os.environ["MONGO_USER"] = "pytest"

from bson import ObjectId
from squirrel.org_model import Org, InventoryDevice


# Insert Data
org_object = Org(
    name="org LV",
    creator="Jim",
    country="TW",
    time_zone="UTC8+",
)
org_object.inventory.aps = [InventoryDevice(id="0"), InventoryDevice(id="1"), InventoryDevice(id="2")]
org_object.save()
print(f"Before Query: {org_object.inventory.aps}")

# DB query
target_device_id = "0"
org_query = {
    "$pull": {
        "inventory.aps": {"id": target_device_id}
    }
}
Org._get_collection().update_one({"_id": org_object.id}, org_query, session=None)

# Reload result
org_object.reload()
print(f"After Query: {org_object.inventory.aps}")

