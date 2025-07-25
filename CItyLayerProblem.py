# need a function to calculate the vector between two points
# need a function to calculate the angle between two vectors



def GetVectorConstructor(dim , dim_name):
    def CreateVector(**kwargs):
        vector = {}
        if(len(kwargs) != dim):
            raise Exception("dimension mismatch")
        for key , val in kwargs.items():
            # TODO: check the var type of key an val
            # they should be str and float
            if not key in dim_name:
                raise Exception("dimension name mismatch")
            vector[key] = val
        vector["dim"] = dim 
        vector["dim_name"] = [x for x in dim_name]
        return vector
    return CreateVector


# this will give you the vectorbetween two points
# if we have points or origin vectors OA and OB
# this function will give you the OA - OB, assuming the first parameter passed was OA
def GetResultantVector(vec2 , vec1):
    if not CheckIfTwoVectorsFallInTheVectorSpace(vec2 , vec1):
        return None , False
    vector_constructor = GetVectorConstructor(vec2['dim'] , vec2['dim_name'])
    resultant_vector = {}
    for dim_n in vec2['dim_name']:
        resultant_vector[dim_n] = vec2[dim_n] - vec1[dim_n]
    return vector_constructor(**resultant_vector), True


def CheckIfTwoVectorsFallInTheVectorSpace(vec2 , vec1):
    vecDimMismatch = Exception('vector dimension mismatch')
    vecDimNameMismatch = Exception('vector dimension name mismatch')
    try:
        if vec2['dim'] != vec1['dim']:
            raise vecDimMismatch
        if len(vec2['dim_name']) != len(vec1['dim_name']):
            raise vecDimMismatch
        dim_set = set()
        for v2_dim in vec2['dim_name']:
            dim_set.add(v2_dim)
        for v1_dim in vec1['dim_name']:
            if not v1_dim in dim_set:
                raise vecDimNameMismatch
        return True
    except:
        return False






vectors_2D = GetVectorConstructor(2 , ['x' , 'y'])

vec1 = vectors_2D(x = 1 , y = 2)
vec2 = vectors_2D(x = 4 , y = 5)
print(GetResultantVector(vec2 , vec1))




            
