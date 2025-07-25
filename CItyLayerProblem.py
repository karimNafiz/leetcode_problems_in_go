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



vectors_2D = GetVectorConstructor(2 , ['x' , 'y'])

vec1 = vectors_2D(x = 1 , y = 2)
print(vec1)




            
