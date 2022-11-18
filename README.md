# data-enrichment-helper-functions
 Functions for data enrichment assignments and projects

## API/JSON Functions

```python

import pandas as pd
import json
import tmdbsimple as tmdb



def read_and_fix_json(JSON_FILE):
    """Attempts to read in json file of records and fixes the final character
    to end with a ] if it errors.
    
    Args:
        JSON_FILE (str): filepath of JSON file
        
    Returns:
        DataFrame: the corrected data from the bad json file
    """
    try: 
        previous_df =  pd.read_json(JSON_FILE)
    
    ## If read_json throws an error
    except:
        
        ## manually open the json file
        with open(JSON_FILE,'r+') as f:
            ## Read in the file as a STRING
            bad_json = f.read()
            
            ## if the final character doesn't match first, select the right bracket
            first_char = bad_json[0]
            final_brackets = {'[':']', 
                           "{":"}"}
            ## Select expected final brakcet
            final_char = final_brackets[first_char]
            
            ## if the last character in file doen't match the first char, add it
            if bad_json[-1] != final_char:
                good_json = bad_json[:-1]
                good_json+=final_char
            else:
                raise Exception('ERROR is not due to mismatched final bracket.')
            
            ## Rewind to start of file and write new good_json to disk
            f.seek(0)
            f.write(good_json)
           
        ## Load the json file again now that its fixed
        previous_df =  pd.read_json(JSON_FILE)
        
    return previous_df
	
	
	
	

def write_json(new_data, filename): 
    """Adapted from: https://www.geeksforgeeks.org/append-to-json-file-using-python/"""    
    
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        ## Choose extend or append
        if (type(new_data) == list) & (type(file_data) == list):
            file_data.extend(new_data)
        else:
             file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file)
```
___
## DataFrame/File Size & File Info Functions

```python
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
```