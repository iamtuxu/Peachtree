import numpy as np
import time
import scipy.stats

MIN = 0.00001


def getMaximum2(a, b):
    if a >= b:
        return a
    else:
        return b


def getMaximum3(a, b, c):
    if a >= b:
        return getMaximum2(a, c)
    else:
        return getMaximum2(b, c)


def fabs(a):
    res = a
    if a < 0:
        res = -1 * a
    return res


def equal(a, b):
    if fabs(a - b) < MIN:
        return True
    else:
        return False


def randomNormalVariable(mean, SD):
    t = int(round(time.time() * 1000)) % 4294967296
    np.random.seed(t)
    res = np.random.normal(mean, SD, 1)
    if res[0] < 0:
        res[0] = 0
    return res[0]

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h