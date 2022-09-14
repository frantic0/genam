import sys

import salome
salome.salome_init()

# Set file paths for library and tests  
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/tests')

from genam.configuration.lens import configurator as lens_configurator
from genam.parametric_shape import parameterize_2D_inner_shape_no_radii, parameterize_2D_inner_shape
from matrices.quantized_1_1 import quantized_matrix_1_1_x

wavelenght = 8.661
brick_ID = 15

lens_config = lens_configurator( quantized_matrix_1_1_x( brick_ID ) )

# Sketch_1 = parameterize_2D_inner_shape( wavelenght,
#                                                  lens_config[0][0][1] * wavelenght,
#                                                  lens_config[0][0][2] * wavelenght )

Sketch_2 = parameterize_2D_inner_shape_no_radii( wavelenght,
                                                 lens_config[0][0][1] * wavelenght,
                                                 lens_config[0][0][2] * wavelenght )


