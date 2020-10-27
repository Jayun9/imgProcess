import process as pc
import json as js

json_path = './exports'
json_merge = pc.ProcessJSON()
json_merge.jsonFileMerge(json_path)
json_file = json_merge.jsonMerge

with open('./merge.json', 'w') as f:
    js.dump(json_file, f)