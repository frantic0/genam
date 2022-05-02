

mesh_configs = {
  'maxSize':      [ 5,     3,    3,    3,    3,    1    ],
  'minSize':      [ 1,     0.8,  0.5,  0.3,  0.08,  0.1 ],
  'secondOrder':  [ True,  True, True, True, True, True ],
  'fineness':     [ 4,     4,    4,    4,    4,    4    ] 
}

selector = lambda i:  ( 
  mesh_configs['maxSize'][i],
  mesh_configs['minSize'][i],
  mesh_configs['secondOrder'][i],
  mesh_configs['fineness'][i],
) 

