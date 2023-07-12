import os
os.environ['MONGO_MOCK'] = "true"
os.environ["MONGO_DB_NAME"] = "pytest"
os.environ["MONGO_USER"] = "pytest"

from bson import ObjectId
from squirrel.org_model import Org
from squirrel.hierarchy_view_model import HierarchyView


# Insert Data
network_ids = [str(ObjectId()) for _ in range(3)]
hierarchy_views = [HierarchyView(name="hv LV", network_ids=network_ids)]
org_object = Org(
    name="org LV",
    creator="Jim",
    country="TW",
    time_zone="UTC8+",
    hierarchy_views=hierarchy_views,
)
org_object.save()
print(f"Before Query: {org_object.hierarchy_views[0].network_ids}")

# DB query
target_network_id = network_ids[0]
org_query = {
    "$push": {
        "hierarchy_views.0.network_ids": "test123"
    }
}
Org._get_collection().update_one({"_id": org_object.id}, org_query, session=None)

# Reload result
org_object.reload()
print(f"After Query: {org_object.hierarchy_views[0].network_ids}")

