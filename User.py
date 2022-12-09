import csv
import random
import pandas as pd

def generate_random_user() :
    
    
        firsts = pd.read_csv('first.csv')
        f=random.randrange(1,len (firsts))

        f_name= firsts['Name'].values[f]
        
    
        lasts = pd.read_csv('first.csv')
        l=random.randrange(1,len (lasts))

        l_name= lasts['Name'].values[l] 
    
        return  (f'{f_name}_{l_name}_{l}')   


