import math 
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

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



def GetAngleWrapper(vec2 , vec1):
    rad , flag = GetSignedAngle2D(vec1 , vec2)
    if not flag:
        return None 
    return RadiansToDegrees(rad)



def GetSignedAngle2D(vec2, vec1):
    if not CheckIfTwoVectorsFallInTheVectorSpace(vec2, vec1):
        return None, False
    
    # Only supports 2D vectors
    if vec2["dim"] != 2 or set(vec2["dim_name"]) != {"x", "y"}:
        raise Exception("Only 2D vectors with 'x' and 'y' components are supported.")

    x1, y1 = vec1["x"], vec1["y"]
    x2, y2 = vec2["x"], vec2["y"]

    dot = x1 * x2 + y1 * y2
    det = x1 * y2 - y1 * x2  # determinant (like 2D cross product)

    angle_radians = math.atan2(det, dot)
    return angle_radians, True

def RadiansToDegrees(radians):
    return math.degrees(radians)

def ParseListToVectors(list_dicts, callback):
    return map(lambda d: callback(**d), list_dicts)

vector_2d = GetVectorConstructor(2 , ['x' , 'y'])


class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length)
        body_str = raw_body.decode('utf-8')
        print("Raw body string:", body_str)
        try:
            data = json.loads(body_str)
            print("Parsed JSON:", data)
            # print("firest data point ", type(data[0]))
            test = ParseListToVectors(data , vector_2d)
            for item in test:
                print(item)
            print("printing out the test variable ")
            print(test)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        # 5. Respond with something
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"status": "received", "data": data}
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run():
    server = HTTPServer(('0.0.0.0', 8080), MyHandler)
    print("Listening on http://localhost:8080")
    server.serve_forever()
run()

# vectors_2D = GetVectorConstructor(2 , ['x' , 'y'])

# vec1 = vectors_2D(x = 1 , y = 2)
# vec2 = vectors_2D(x = 4 , y = 5)

# print(GetAngleWrapper(vec2 , vec1))







































            
