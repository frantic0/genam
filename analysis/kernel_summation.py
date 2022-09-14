from paraview.simple import *

reader1 = OpenDataFile("C:/SAN/uclic/ammdgop/data/quantized_matrix_2_2_15_x_x_x/2_2_15_x_x_x.vtu")
reader2 = OpenDataFile("C:/SAN/uclic/ammdgop/data/quantized_matrix_2_2_x_x_0_x/2_2_x_x_0_x.vtu")
reader3 = OpenDataFile("C:/SAN/uclic/ammdgop/data/quantized_matrix_2_2_15_x_0_x/2_2_15_x_0_x.vtu")

reader1.UpdatePipeline()
reader2.UpdatePipeline()
reader3.UpdatePipeline()


appendDatasets = AppendDatasets(Input=[reader1, reader2, reader3])