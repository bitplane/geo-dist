


1. get geonames tsv dump
2. extract places
3. stick them into a tree based on geohash
4. find distance between them
5. try to route between nearby places
   openrouteservice with this for now:
   https://download.geofabrik.de/europe/great-britain-latest.osm.pbf
6. if the distance is close to the tree node size, collapse segment


lookup:

drill down into tree.
5 digits should be enough.
width and height alternates 4x8, 8x4

