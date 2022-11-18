import os
def get_df_memory_usage(df,units='mb'):
	"""returns memory size of dataframe in requested units"""
	memory = df.memory_usage().sum()
	if units.lower()=='mb':
		denom = 1e6
	elif units.lower()=='gb':
		denom = 1e9
	elif units.lower()=='kb':
		denom = 1e3
	else:
		raise Exception('Units must be either "mb" or "gb"')
	val = memory/denom
	print(f"- Total Memory Usage = {val} {units.upper()}")
    
    
def get_filesize(fname, units='mb'):
	"""Get size of file at given path in MB or GB"""
	if units.lower()=='mb':
		denom = 1e6
	elif units.lower()=='gb':
		denom = 1e9
	elif units.lower()=='kb':
		denom = 1e3
	else:
		raise Exception('Units must be "kb","mb", or "gb"')
		
	import os
	size = os.path.getsize(fname)

	val = size/denom
	# str_val = f"{val} {units.upper()}"
	print(f"- {fname} is {val} {units.upper()} on disk.")

	return val
	

def get_file_info(fname, units='mb'):
	"""Returns a dictionary with detailed file information including:
	- File name, extension, file size, date created, date modified, etc.
	Args:
		fname (str): filepath
		units (str, optional): Units for fileszize. (Options are "kb','mb','gb'). Defaults to 'mb'.

	Returns:
		dict: dictionary with info
	"""
	import time
	import os
	import pandas as pd
	
	## Get file created and modified time
	modified_time = time.ctime(os.path.getmtime(fname))
	created_time = time.ctime(os.path.getctime(fname))
	
	## Get file size 
	raw_size = os.path.getsize(fname)
	size = get_filesize(fname,units=units)
	str_size = f"{size} {units}"
	
	# Get path info
	rel_path = os.path.relpath(fname)
	abs_path =  os.path.abspath(fname)
	_, ext = os.path.splitext(fname)
	basename =os.path.basename(fname)
	dirname = os.path.dirname(fname)
	
	file_info ={"Filepath": fname,"Name":basename, 'Created':created_time, 'Modified':modified_time,  'Size':str_size,
	'Folder':dirname,"Ext":ext, "Size (bytes)":raw_size,
	'Relative Path':rel_path,'Absolute Path':abs_path}
	
	return file_info