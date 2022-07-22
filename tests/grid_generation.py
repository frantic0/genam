import numpy as np



min, max, step = 0, 16, 1

space = []

for w in np.arange(min, max, step):  
    for x in np.arange(min, max, step): 
        for y in np.arange(min, max, step):
            for z in np.arange(min, max, step): 
                space.append([w,x,y,z])

print(len(space))
#print(*sample, sep='\n')

