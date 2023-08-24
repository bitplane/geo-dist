
# Finding the distance between two places

Find the distance between two places.

1. get geonames tsv dump
2. extract places
3. stick them into a tree based on geohash
4. find distance between them
5. try to route between nearby places
   openrouteservice with this for now:
   https://download.geofabrik.de/europe/great-britain-latest.osm.pbf
6. if the distance is close to the tree node size, collapse segment


## notes

-30 is a longitude that doesn't intersect any islands other than
greenland but there's no roads in most of the country.


class QuadTreeNode:
   """

   """
   def __init__(self, y=0.0, x=0.0, value=None, leaf=False):
      self.is_leaf = leaf
      self.nodes = [None, None, None, None]
      self.y = y
      self.x = x
      self.value = value
      self.needs_rebalance = False

   def balance(self):
      """
      Balance all the nodes under this one
      """
      if self.is_leaf or not self.needs_rebalance:
         return

      # balance all the nodes under this one
      for node in self.nodes:
         if node:
            node.balance()
      
      # get the average position of our children
      nodes = [node for node in self.Nodes if node]
      self.y = sum([node.y for node in nodes]) / len(nodes)
      self.x = sum([node.x for node in nodes]) / len(nodes)

   def add(self, lat, lon, value=None):
      """
      External function to add a new node to the tree.
      """
      y, x = location_to_quadtree(lat, lon)
      node = QuadTreeNode(y, x, value, leaf=True)
      self._add(node)

   def _add(self, node):
      """
      Add a node internally
      """

      if self.is_leaf:
         new_node = QuadTreeNode(self.y, self.x, self.value, leaf=True)
         self.is_leaf = False
         self.nodes = [None, None, None, None]
         self.x = self.y = self.value = None

         self._add(new_node)

      pos_y = 0 if node.y < self.y else 2
      pos_x = 0 if node.x < self.x else 1
      idx = pos_y + pos_x

      if not self.nodes[idx]:
         self.nodes[idx] = node
      else:
         self.nodes[pos]._add(node)

      self.balance()

   def location_to_quadtree(lat, lon):
      """
      Normalize a latitude/longitude pair to a quadtree coordinate.
      We use -30 as the center of the map, which is the middle of the
      atlantic ocean and doesn't intersect any land masses other than
      greenland, which is mostly ice and has few roads.
      """
      y = (lat + 90) / 180
      x = (lon + 150) / 360

      return y, x
