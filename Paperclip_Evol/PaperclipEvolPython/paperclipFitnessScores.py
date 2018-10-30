

import numpy as np




def FitnessTest(indivs, fitType):
	# This function is called for an indivs (individuals) matrix of size (any, numSeg, 3)
	# Call the appropriate fitness score
	if fitType == 1:
		scores = FScore1(indivs)
	if fitType == 2:
		scores = FScore2(indivs)
	if fitType == 3:
		scores = FScore3(indivs)

	# Now, we need to rank the individuals according to the fitness score. 
	combined = zip(scores, indivs)
	sortedScores = sorted(combined, reverse=True)
	rScores, rIndivs = zip(*sortedScores)

	return np.asarray(rScores), np.asarray(rIndivs)



def vecTransform(rotMatrixIndiv):
	# Takes a single individual that is in rotational notation and converts them to vector notation
	vecMatrixIndiv = np.zeros(rotMatrixIndiv.shape)
	# We need the "seed" vector for the first set of rotations to apply onto. We choose (0,0,1)
	oldVec = np.array([0,0,1])

	for i in range(rotMatrixIndiv.shape[0]):
		# For reading ease, we rename the rotations and previous vector for case i.
		rotx = rotMatrixIndiv[i,0]
		roty = rotMatrixIndiv[i,1]
		rotz = rotMatrixIndiv[i,2]
		x = oldVec[0]
		y = oldVec[1]
		z = oldVec[2]
		# We now calculate the new vector.
		# The below was calculated on mathematica using the 3D rotation matrices found here: https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
		# We are performing rotx first, then roty, then rotz
		vecMatrixIndiv[i,0]= np.sin(rotx)*(y*np.sin(roty)*np.cos(rotz) + z*np.sin(rotz)) + np.cos(rotx)*(z*np.sin(roty)*np.cos(rotz) - y*np.sin(rotz)) + x*np.cos(roty)*np.cos(rotz);
		vecMatrixIndiv[i,1]= np.sin(rotz)*(y*np.sin(rotx)*np.sin(roty) + x*np.cos(roty)) + np.cos(rotx)*(z*np.sin(roty)*np.sin(rotz) + y*np.cos(rotz)) - z*np.sin(rotx)*np.cos(rotz)
		vecMatrixIndiv[i,2]= y*np.sin(rotx)*np.cos(roty) + z*np.cos(rotx)*np.cos(roty) - x*np.sin(roty)
		# Store this vector to grow the next segment
		oldVec = vecMatrixIndiv[i]

	return vecMatrixIndiv




def FScore1(indivs):
	"""
	This class calculates a fitness score that corresponds mathematically to the discrete curl of the antenna. We take the z-component of the cross-product of every two adjacent vectors, and sum them up for the fitness score. An ideal antenna will be coplanar with the x-y plane, and will be a square coil.
	"""
	# First, we need to convert from rotations to unit vector coordinates.
	# Each unit vector corresponds to the direction that line segment is pointing relative to fixed coordinates. We then calculate the cross product, take the z component, and store it in fScores.
	fScores = np.zeros((indivs.shape[0]))
	for i in range(indivs.shape[0]):
		# First, calculate the vector form of the individual i
		vecForm = vecTransform(indivs[i])
		# Now, we can calculate the cross products
		# We are taking the z-component of each of the numseg-1 corners of the antenna. 
		zComp = 0.0
		for j in range(indivs.shape[1]-1):
			zComp += np.cross(vecForm[j], vecForm[j+1])[2]
		# This z-component is the fitness score for antenna i.
		fScores[i] = zComp

	return fScores
		


def FScore2(indivs):
	# Just a dummy fscore for now
	return np.arange(indivs.shape[0])









