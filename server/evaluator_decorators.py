from functools import wraps

_ANALYTIC_DEPTH_REGISTRY = {}

def enforce_depth(required_depth, analytic_name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.check_circuit_depth(required_depth, analytic_name or func.__name__)
            return func(self, *args, **kwargs)
        wrapper._circuit_depth = required_depth
        wrapper._analytic_name = analytic_name or func.__name__
        _ANALYTIC_DEPTH_REGISTRY[wrapper._analytic_name] = wrapper._circuit_depth
        return wrapper
    return decorator

def get_analytic_depth_registry():
    return dict(_ANALYTIC_DEPTH_REGISTRY)