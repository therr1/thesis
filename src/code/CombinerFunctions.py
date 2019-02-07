import numpy as np

class FunctionGetter:

    def get_function(name):
        if name == "dot":
            return lambda x,y : np.dot(x,y)


# x = np.array([1,2,3])
# y = np.array([2,3,4])

# call_back = FunctionGetter.get_function("dot")
# print(call_back(x,y))