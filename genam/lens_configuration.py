import numpy as np

flaps_configs = { 
  'length':   [0, .062, .092, .112, .132, .152, .162, .171, .191, .221, .241, .251, .271, .281, .301, .321],
  'distance': [0, .216, .212, .207, .189, .161, .166, .171, .134, .257, .234, .230, .207, .203, .175, .152],  
  'radius':   [0, .062, .092, .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1] 
}

unit_cell_select_list = lambda i: np.array([
                                flaps_configs['length'][i], 
                                flaps_configs['distance'][i], 
                                flaps_configs['radius'][i] 
                              ])


def lens_configurator( quantized_matrix ):
  # create configs matrix with shape (m,n,3)
  configs = np.array([ unit_cell_select_list(i) for i in quantized_matrix.ravel() ])
  # reshape configs matrix into shape (m,n,3)
  configs_to_stack = configs.reshape(quantized_matrix.shape[0], quantized_matrix.shape[1], len(flaps_configs) )  
  # stack configs to quantised matrix to get [ [ [ phase_id, flap length, flap distance, radius ] ] ]
  return np.dstack( ( quantized_matrix, configs_to_stack ) )