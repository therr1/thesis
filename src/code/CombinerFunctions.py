import numpy as np

class FunctionGetter:

    def get_function(name, rinverse=None):
        if name == "dot":
            return lambda x,y : np.dot(x,y)

        if name == "corr":
            def compute_corr(x,y):
                return x.dot(rinverse).dot(y)
            if rinverse is None:
                return lambda x,y : np.dot(x,y)

            return compute_corr



# x = np.array([1,2,3])
# y = np.array([2,3,4])

# call_back = FunctionGetter.get_function("dot")
# print(call_back(x,y))
