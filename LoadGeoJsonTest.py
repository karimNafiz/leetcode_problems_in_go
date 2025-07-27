import json

# Load entire GeoJSON into memory
with open('mtlbld_v4.geojson', 'r') as f:
    geojson_data = json.load(f)

# Create an iterator over the features list
features_iter = iter(geojson_data['features'])

# Get the next feature
first_feature = next(features_iter)
print('first feature type ', type(first_feature['geometry']['coordinates']))
print("First feature geometry:", first_feature['geometry']['coordinates'][0][0])
#print("First feature properties:", first_feature['properties'])

# # Get the second feature (if exists)
# second_feature = next(features_iter)
# print("Second feature geometry:", second_feature['geometry'])
