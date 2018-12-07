import numpy as np

def month_rate_to_irr(nper, mrate):
    return np.rate(nper, 1/12+mrate, -1, 0) * 12

def irr_to_month_rate(nper, yrate):
    '''
    >>> round(irr_to_month_rate(12, 0.1095), 6)
    0.005025
    '''
    return np.pmt(yrate/12, nper, -1) - 1/12

def xy_plan(pv, xrate, xnper, yrate, ynper):
    '''
    >>> xy_plan(10000, 0.1095/12, 6, irr_to_month_rate(12, 0.1095), 12)
    [-10000, 91.25, 91.25, 91.25, 91.25, 91.25, 91.25, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147, 883.5833766754147]
    '''
    r = [-pv, ]
    x1 = pv*xrate
    y1 = pv*yrate + pv*1.0 / ynper
    for i in range(xnper):
        r.append(x1)
    for i in range(ynper):
        r.append(y1)
    return r

def xy_irr(xrate, xnper, yrate, ynper):
    '''
    >>> np.irr([-10000,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33])
    0.01788040887559883
    >>> round(xy_irr(0.1095/12, 6, irr_to_month_rate(12, 0.1095), 12) * 12, 6)
    0.1095
    '''
    pv = 10000
    plan = xy_plan(pv, xrate, xnper, yrate, ynper)
    return np.irr(plan)

def xy_diff_plan(pv, xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2):
    '''
    >>> xy_diff_plan(20000, 0.011, 6, 0.011, 12, 0.1095/12, 6, irr_to_month_rate(12, 0.1095), 12)
    [-20000, 37.5, 37.5, 37.5, 37.5, 37.5, 37.5, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738]
    '''
    plan1 = xy_plan(pv, xrate1, xnper1, yrate1, ynper1)
    plan2 = xy_plan(pv, xrate2, xnper2, yrate2, ynper2)
    plan = (np.array(plan1) - np.array(plan2)).tolist()
    plan[0] = -pv
    return plan

def xy_diff_irr(xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2):
    '''
    >>> round(xy_diff_irr(0.011, 6, 0.011, 12, 0.1095/12, 6, irr_to_month_rate(12, 0.1095), 12), 5)
    0.07758
    '''
    pv = 10000
    plan = xy_diff_plan(pv, xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2)
    for i in range(xnper2+1, len(plan)):
        plan[i] = plan[i] + pv / ynper2
    return np.irr(plan) * 12

if __name__ == "__main__":
    import doctest
    doctest.testmod()
