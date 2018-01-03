import contextlib

import torch
import torch.autograd as autograd

from machina.misc import logger

# default gpu_id is -1.
# this means using cpu
_GPU_ID = -1

def set_gpu(device_id):
    global _GPU_ID
    _GPU_ID = device_id


def get_gpu():
    return _GPU_ID


@contextlib.contextmanager
def cpu_mode():
    """
    contextmanager
    set _GPU_ID to -1 while cpu_mode
    """
    global _GPU_ID
    tmp = _GPU_ID
    _GPU_ID = -1
    yield
    _GPU_ID = tmp


@contextlib.contextmanager
def measure(name):
    import time
    s = time.time()
    yield
    e = time.time()
    logger.log("{}: {:.4f}sec".format(name, e-s))


def torch2torch(tensor):
    """
    torch tensor with wrapping cuda
    """
    if _GPU_ID != -1:
        return tensor.cuda(_GPU_ID)
    else:
        return tensor


def np2torch(ndarray):
    """
    transform ndarray to torch tensor with cuda
    """
    return torch2torch(torch.from_numpy(ndarray))


class Variable(autograd.Variable):
    def __init__(self, data, *args, **kwargs):
        data = torch2torch(data)
        super(Variable, self).__init__(data, *args, **kwargs)
