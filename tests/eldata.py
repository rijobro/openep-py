
import scipy.io as sio
from scipy.interpolate import Rbf
from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt

# interpolation function
'''
Parameters:
------------
x0 – Cartesian co-ordinates of the data points
d0 – Data values; voltage values
x1 – the locations at which you want data (mesh nodes)

Return:
interpolated values (voltage values at each mesh node)
'''
def interpolate(method,x0, d0, x1):


    # remove any data with NaNs
    # d0 = d0[~np.isnan(d0)]
    print('inside interpolate',d0.shape)
    # x0 = x0[~np.isnan(x0)]
    print('inside interpolate x0',x0[:,0].shape)
    # print('do:',x0[0:10,0])
    # perform interpolation - scatteredinterpolant
    rbfi = Rbf(x0[:,0],x0[:,1],x0[:,2],d0,function='gaussian')

    # rbfi = Rbf(np.linalg.pinv([x0[:,0],x0[:,1],x0[:,2],d0]))
    # X, Y, Z = np.meshgrid(x, y, z)
    # I = RBFInterpolant(x0, d0, sigma=0.1, phi='phs2', order=1)



        # match method:
        # case 'scatteredinterpolant':
        # print('scatteredinterpolant')





    d1 = 0
    return d1






# DEFINITIONS
amplitude = 'max'


# Loading Electroanatomic mapping data
file_path = '../tests/data/openep_dataset_1.mat'



# Load the file
# Main MAT File - userdata
main_file = sio.loadmat(file_path)

# Anatomical Data - mesh descriptions(vertices & triangles)
# Vertices/Points = .X
data_tri_X = main_file['userdata']['surface_triRep_X'][0][0]
x = data_tri_X[:,0]
y = data_tri_X[:,1]
z = data_tri_X[:,2]


# Triangulation/faces - .T
data_tri_T = main_file['userdata']['surface_triRep_Triangulation'][0][0]
# Resolving indexing issue - matlab to python
t = data_tri_T-1

# Electric data (Userdata.Electric)
electric =  main_file['userdata']['electric'][0][0][0][0]

# Locations - cartesian coordinates
egmSurfX = np.array(electric[13])
print('egmSurfX\n', egmSurfX)
point_x = egmSurfX[:,0]
point_y = egmSurfX[:,1]
point_z = egmSurfX[:,2]

# Voltage - time series of electrogram voltages
egm = np.array(electric[4])
print('egm\n',egm)
# duration - milliseconds
egm_duration = egm.shape[1]

# Window of interest
# Annotations Struct (UserData.Electric.Annotations)
annotations = electric[10][0][0]

# Reference annotation
ref = np.array(annotations[1])
print('window of interest - ref\n',ref)

# woi
woi = np.array(annotations[0])
print('woi\n',woi)

# Extract the region of the electrogram of interest for each mapping point
region_of_interest = ref + woi
print('region of interest\n',region_of_interest)

# For each mapping point, n, find the voltage amplitude
#  - Apply the user defined function (for example max(egm) – min(egm))
max_volt=[]
min_volt=[]

for volt in egm:
    max_volt.append(np.amax(volt))
    min_volt.append(np.amin(volt))

max_volt = np.array(max_volt)
min_volt = np.array(min_volt)


amplitude_volt = max_volt - min_volt
print(amplitude_volt.shape)
print('voltage-max\n',max_volt)
print('voltage-min\n',min_volt)


#  - Set of voltage values with a set of associated x y z values / node indices
data_set = np.transpose(np.array([amplitude_volt,point_x,point_y,point_z]))
print('dataset\n',data_set)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# plt.plot(egm)
# plt.plot(amplitude_volt)
plt.scatter(point_x,point_y,point_z)
# plt.scatter(,z)
plt.show()


# Interpolate the voltage values across the shell

method = 'scatteredinterpolant'
# x0 = data_set[:,1:4]
# d0 = data_set[:,0]


x0 = egmSurfX
d0 = amplitude_volt
x1 = data_tri_X

print('x0\n',x0)
print('d0\n',d0)
print(x1)

out = interpolate(method,x0, d0, x1)

















#
#
# fig = plt.figure(constrained_layout=True,
#                  frameon=True,
#                  figsize=(40,20), dpi=80)
# # first plot
# # get the current 3d axis on the current fig
# ax1 = fig.add_subplot(1,1,1, projection='3d')
#




# print('max voltage:\n',max_volt)
