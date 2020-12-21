expand_count = 0

def expand(node, _map): 
	global expand_count
	expand_count = expand_count + 1
	return [next for next in _map[node] if _map[node][next] is not None]