import math
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# don't use classes in python xD
def make_vector_factory(dim: int, dim_names: list[str]):
    def create_vector(**kwargs):
        if len(kwargs) != dim:
            raise ValueError("Dimension mismatch: expected %d keys" % dim)
        vector = {}
        for key, val in kwargs.items():
            if not isinstance(key, str) or not isinstance(val, (int, float)):
                raise TypeError("Key must be str and value must be float or int")
            if key not in dim_names:
                raise ValueError(f"Unexpected dimension name: {key}")
            vector[key] = float(val)
        vector["dim"] = dim
        vector["dim_name"] = list(dim_names)
        return vector
    return create_vector


def subtract_vectors(v1, v2):
    if not are_vectors_compatible(v1, v2):
        raise ValueError("Vectors are not in the same vector space")

    factory = make_vector_factory(v1['dim'], v1['dim_name'])
    diff = {dim: v1[dim] - v2[dim] for dim in v1['dim_name']}
    return factory(**diff)


def are_vectors_compatible(v1, v2):
    try:
        return (
            v1['dim'] == v2['dim'] and
            set(v1['dim_name']) == set(v2['dim_name'])
        )
    except (KeyError, TypeError):
        return False


def signed_angle_2d(from_vec, to_vec):
    if not are_vectors_compatible(from_vec, to_vec):
        raise ValueError("Incompatible vectors for angle calculation")

    if from_vec["dim"] != 2 or set(from_vec["dim_name"]) != {"x", "y"}:
        raise ValueError("Only 2D vectors with dimensions 'x' and 'y' are supported")

    x1, y1 = from_vec["x"], from_vec["y"]
    x2, y2 = to_vec["x"], to_vec["y"]

    dot = x1 * x2 + y1 * y2
    det = x1 * y2 - y1 * x2

    return math.atan2(det, dot)


def radians_to_degrees(rad):
    return math.degrees(rad)


def angle_between_vectors(from_vec, to_vec):
    try:
        rad = signed_angle_2d(from_vec, to_vec)
        return radians_to_degrees(rad)
    except Exception as e:
        return None


def parse_vectors(vector_dicts, vector_factory):
    return [vector_factory(**vec) for vec in vector_dicts]


def total_rotation_angle(vector_list):
    if len(vector_list) < 3:
        raise ValueError("At least 3 vectors are required for angle calculation")

    origin = vector_list[0]
    prev = subtract_vectors(origin, vector_list[1])
    total_angle = 0

    for vec in vector_list[2:]:
        current = subtract_vectors(origin, vec)
        angle = angle_between_vectors(prev, current)
        if angle is None:
            raise ValueError("Failed to calculate angle between vectors")
        print('calculated angle ',angle)
        total_angle += angle
        prev = current

    return total_angle


class VectorHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            data = json.loads(raw_body.decode('utf-8'))

            vector_factory = make_vector_factory(2, ['x', 'y'])
            vectors = parse_vectors(data, vector_factory)

            angle = total_rotation_angle(vectors)

            response = {
                "status": "success",
                "angle_sum_degrees": angle
            }

            self._send_response(200, response)

        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
        except ValueError as e:
            self._send_response(400, {"error": str(e)})
        except Exception as e:
            self._send_response(500, {"error": f"Internal server error: {str(e)}"})

    def _send_response(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def run_server():
    server = HTTPServer(('0.0.0.0', 8080), VectorHandler)
    print("Listening on http://localhost:8080")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
    # vector_2d_constructor = make_vector_factory(2 , ['x' , 'y'])
    # vec1 = vector_2d_constructor(x=1 , y=1)
    # vec2 = vector_2d_constructor(x=4 , y=5)
    # vec3 = subtract_vectors(vec2 , vec1)
    # angle = angle_between_vectors(vec1 , vec2)
    # print(angle)
    #print(vec3)