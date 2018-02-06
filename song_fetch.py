from grab_lyrics import *
from universal import Universal

import os

universe = Universal()

raw_counts_dir_name = universe.raw_counts_dir_name
normalized_dir_name = universe.normalized_dir_name
delimiter = universe.delimiter
links_dir_name = universe.links_dir_name

for filename in os.listdir(links_dir_name):
    file = open(links_dir_name + "/" + filename, "r")
    contents = file.read()
    file.close()

    genre = filename.split(".")[0]
    links = contents.split()
    write_dicts(genre, links)
