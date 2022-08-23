from utility_functions import * 
# from brick import * 
from parametric_shape import * 

###
### Salome GEOM and SMESH components
###

import salome
import GEOM

from salome.geom import geomBuilder
import SALOMEDS

import SMESH, SALOMEDS
from salome.smesh import smeshBuilder
from salome.GMSHPlugin import GMSHPluginBuilder




class Pipeline:
  
  def __init__( self,
                name = 'lens',
                wavelength = 8.661
              ) -> None :

                # mesh_config,
                # set_hemisphere = False
                # set_PML = True,
                # source_config = None,
                # inlet_offset = 0.001,
                # outlet_offset = 0.001,
    pass


  def add( self, component ) -> None: 
    pass


  def remove( self, at ) -> None: 
    pass


  def processGeometry( self ) -> None:
    pass


  def processMesh( self ) -> None:  
    pass

  def exportMesh( self ) -> None:
    pass  