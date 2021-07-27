import pandas as pd
import numpy as np
import requests
from PIL import Image
import io
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import json
import argparse

def requests_PIL_download(id_tuple):
    thumb_size = (500,500)
    ids_id, image_url = id_tuple
    width, height = np.nan, np.nan
    filename = 'data/images/{}.jpg'.format(ids_id)

    try:
        r = requests.get(image_url, timeout=60)
        if r.headers['Content-Type'] == 'image/jpeg':
            try:
                with Image.open(io.BytesIO(r.content)) as im:
                    width, height = im.size
                    im.thumbnail(thumb_size)
                    im.save(filename)
            except:
                print('Weird error with ' + ids_id)
    except:
        print('Timeout error with ' + ids_id)
    return {'width': width, 'height': height, 'ids_id': ids_id}


ap = argparse.ArgumentParser()
ap.add_argument('-t', "--edan_tsv", required=True,
                help="file path containing image data in TSV format")
ap.add_argument("-p", "--processes",
                help="number of processes")
ap.add_argument("-d", "--dim-file",
                help="file path for dimension tsv output")
args = ap.parse_args()

edan_image_df = pd.read_csv(args.edan_tsv, sep='\t')
image_tuples = list(edan_image_df[['ids_id','image_url']].to_records(index=False))

start_time = time.perf_counter()

dimension_list = []

# for image_tuple in image_tuples:
#     print(image_tuple)
#     dimensions = requests_PIL_download(image_tuple)
#     dimension_list.append(dimensions)

with ThreadPoolExecutor(max_workers=int(args.processes)) as executor:
    dimension_list = list(executor.map(requests_PIL_download, image_tuples))

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Downloaded {len(dimension_list)} images in {elapsed_time} s")

dimension_df = pd.DataFrame(dimension_list)
dimension_df.to_csv(args.dim_file, index=False, sep='\t')