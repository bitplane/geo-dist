
# Finding the distance between two places

Find the distance between two places.

## Steps

Run `make` and it will:

1. Install python deps. Gigs of Python ML deps in here
2. download geonames tsv dump. This is a 1.7gb download.
3. Extract places where people actually live. 25 million rows to 2m.
   Takes 10 minutes or so.
4. Build a quadtree over the nodes in the database. A couple of mins.
5. Extract pairs of nodes that are within routing distance. Needs to
   generate about 50m records, takes about 60 hours. Will run in a
   per-country order creating a job for each one. Heavily CPU-bound
   so can be pushed to the cloud. Feel free to abort and continue as
   needed.
6. For each region, it'll download the appropriate openrouteservice
   data file, spin up ors, then check distances for jobs that ran
   in that region. This should take a couple of days.
   Issue here is RAM. The Europe file needs ~60GB. Need to fix this
   by breaking into smaller regions.
7. Once this is complete, we need to do a second pass of node creation
   focused on hot spots. Then run step 8 again!
8. tbc...

Notes:

* If you're on AWS you're gonna run out of space on your rootfs. Create a
  volume of about 200gb, use cfdisk to make tmpfs for /tmp as well as the
  volume for this repo.
* current experiments are under ./notebooks - they'll be moved into the
  project main directory once thrashed out.

## openrouteservice notes

openrouteservice with this for now:
   <https://download.geofabrik.de/europe/great-britain-latest.osm.pbf>

## Running

Look at the Makefile. `make` will attempt to do everything but will
take days to complete (at best).

You can interrupt the process and it'll continue

## notes

-30 is a longitude that doesn't intersect any islands other than
greenland but there's no roads in most of the country.

### ORS

* openrouteservice uses lon,lat not lat,lon:
  <http://localhost:8080/ors/v2/directions/driving-car?start=-0.1526548,51.5375137&end=-0.15689,51.53942>
* needs 2x the RAM of the file you're loading
* `jq '.features[].properties.summary.distance'`
