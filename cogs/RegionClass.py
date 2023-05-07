# Custom class to create Region Objects for the bot
# We need the name (<NAME>), update time(<LASTUPDATE>), delegate (<DELEGATE>),
# endos (<DELEGATEVOTES>), and founder (<FOUNDER>)


import pandas as pd
import numpy as np


class Region:
    def __init__(self, name, update, delegate, endos, founder):
        self.name = name
        self.update = update
        self.delegate = delegate
        self.endos = endos
        self.founder = founder

#file_path = 'region.xml' # We will do this manually later. Tsk tsk. 
#with open(file_path, 'r') as f:
#    df = pd.read_xml(f.read())
#
#
#name = df.iloc[0:1, 0:1]
