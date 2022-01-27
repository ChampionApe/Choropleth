import pandas as pd, json

# MAIN FUNCTION:
def AdjustData(f,label):
	""" Fix data """
	f = fix_labels(f,label)
	return collect_data(f,label),list(unique_labels(f,label))

# Auxiliary functions:
def fix_encoding(x):
    try:
        return x.encode('latin1').decode('utf_8')
    except UnicodeEncodeError:
        return x.replace('Ã†','Æ').replace('Ã¸','ø')

def fix_labels(f,label):
	for n in range(len(f['features'])):
		f['features'][n]['properties'][label] = fix_encoding(f['features'][n]['properties'][label])
	return f

def list_mun_i(fts, mun_i,label):
	return [x for x in fts if x['properties'][label]==mun_i]

def merge_nongeometry(fts_mun_i):
	return {k: fts_mun_i[0][k] for k in fts_mun_i[0] if k != 'geometry'}

def merge_geometry(fts_mun_i):
	return {'type': 'MultiPolygon',
			'coordinates': [fts_mun_i[n]['geometry']['coordinates'] for n in range(len(fts_mun_i))]}

def merge_fts(fts_mun_i):
	if len(fts_mun_i)==1:
		return fts_mun_i[0]
	else:
		return {**merge_nongeometry(fts_mun_i),**{'geometry': merge_geometry(fts_mun_i)}}

def unique_labels(f,label):
	""" Set of all releveant municipalities """
	return set([f['features'][x]['properties'][label] for x in range(len(f['features']))])

def collect_data(f,label):
	return {**{k:v for k,v in f.items() if k!= 'features'}, # simply copy keys that are not 'features'
			**{'features': [merge_fts(list_mun_i(f['features'],mun_i,label)) for mun_i in unique_labels(f,label)]} # for each municipality, perform the merge described above
			}

