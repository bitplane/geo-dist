
# Finding the distance between two places

Find the distance between two places.

1. get geonames tsv dump
2. extract places where people actually live
3. stick them into a quadtree
4. find the closest nodes
5. try to route between nearby places
   openrouteservice with this for now:
   <https://download.geofabrik.de/europe/great-britain-latest.osm.pbf>
6. if the distance is close to the tree node size, collapse segment

## notes

-30 is a longitude that doesn't intersect any islands other than
greenland but there's no roads in most of the country.

### ORS

* openrouteservice uses lon,lat not lat,lon:
  <http://localhost:8080/ors/v2/directions/driving-car?start=-0.1526548,51.5375137&end=-0.15689,51.53942>
* needs 2x the RAM of the file you're loading
