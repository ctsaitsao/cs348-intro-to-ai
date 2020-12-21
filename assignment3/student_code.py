from expand import expand
from operator import itemgetter

# class node:
#     def __init__(self, place, f, h, path_via):        

#         self.place = place
# 		self.f = f
# 		self.h = h
# 		self.path_via = path_via
	
#         return
    
#     def __lt__(self, value):
# 		return self.f < other.f

def a_star_search (dis_map, time_map, start, end):
	path = []
	# TODO Put your code here.
	# be sure to call the imported function expand to get the next list of nodes

	if start not in dis_map:
		return []

	if end not in dis_map:
		return []

	if start == end:
		return [end]

	que_list = []  
	que_list.append({'place': start, 'f': 0, 'h': dis_map[start][end], 'path_via': start})  # f = combined, h = heuristic (distance)
	path_dict = []		# dict that is going to be constructed at the end
	path_dict.append({'place': start, 'f': 0, 'h': dis_map[start][end], 'path_via': start})
	path_dict_places_only = []  # only places of path_dict, to make it a list
	path_dict_places_only.append(start)
	visited = []

	while(True):

		current_node = que_list.pop(0)

		if current_node["place"] in visited:    # keep going
			continue

		if current_node["place"] == end:    # this is where the code ends
			path_dict.append(current_node)
			break

		visited.append(current_node["place"])      

		for node in expand(current_node["place"], time_map):      
				if node in visited:
					if node not in path_dict_places_only:    
						for node2 in que_list:
							if node2['place'] == node:      # reconstruct if found better path
								if node2['f'] > time_map[current_node["place"]][node] + current_node["f"]:
									node2['h'] = time_map[current_node["place"]][node] + current_node["f"] + dis_map[node][end]
									node2['f'] = time_map[current_node["place"]][node] + current_node["f"]
									node2['path_via']: current_node['place']

				else:
					que_list.append({
						'place': node,
						'h': time_map[current_node["place"]][node] + current_node["f"] + dis_map[node][end],
						'f': time_map[current_node["place"]][node] + current_node["f"],
						'path_via': current_node['place']})

		path_dict.append(current_node)
		path_dict_places_only.append(current_node["place"])

		que_list = sorted(que_list, key = itemgetter('h'))
		smalldistance = que_list[0]['h']

		for node2 in que_list:
			if node2["place"] == end:
				if node2["h"] == smalldistance:
					que_list.remove(node2)
					que_list.insert(0, node2)
					break

		# print(que_list)


	path.insert(0, current_node["place"])
	path.insert(0, current_node["path_via"])


	while (current_node["path_via"] != start):

		for node2 in path_dict:
			if node2["place"] == current_node["path_via"]:
				current_node = node2
				break
		path.insert(0, current_node["path_via"])


	return path