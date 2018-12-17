from collections import defaultdict
import numpy as np

def month_rate_to_irr(nper, mrate):
    return np.rate(nper, 1.0/12+mrate, -1, 0) * 12

def irr_to_month_rate(nper, yrate):
    '''
    >>> round(irr_to_month_rate(12, 0.1095), 6)
    0.005025
    '''
    return np.pmt(yrate/12, nper, -1) - 1.0/12

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

def xy_yp_plan(pv, xrate, xnper, yrate, ynper):
    '''
    >>> xy_yp_plan(10000, 0.1095/12, 6, irr_to_month_rate(12, 0.1095), 12)
    [0, 0, 0, 0, 0, 0, 0, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334, 833.3333333333334]
    '''
    r = [-0, ]
    y1 = pv*1.0 / ynper
    for i in range(xnper):
        r.append(0)
    for i in range(ynper):
        r.append(y1)
    return r

def xy_irr(xrate, xnper, yrate, ynper):
    '''
    >>> round(np.irr([-10000,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33]), 5)
    0.01788
    >>> round(xy_irr(0.1095/12, 6, irr_to_month_rate(12, 0.1095), 12) * 12, 6)
    0.1095
    >>> a = np.array([-10000,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33,933.33])
    >>>
    '''
    pv = 10000
    plan = xy_plan(pv, xrate, xnper, yrate, ynper)
    return np.irr(plan)

def xy_diff_plan(pv, xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2):
    '''
    >>> xy_diff_plan(20000, 0.011, 6, 0.011, 12, 0.1095/12, 6, irr_to_month_rate(12, 0.1095), 12)
    [0.0, 37.5, 37.5, 37.5, 37.5, 37.5, 37.5, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738, 119.49991331583738]
    '''
    plan1 = xy_plan(pv, xrate1, xnper1, yrate1, ynper1)
    plan2 = xy_plan(pv, xrate2, xnper2, yrate2, ynper2)
    plan = (np.array(plan1) - np.array(plan2)).tolist()
    #plan[0] = -pv
    return plan

def xy_diff_irr(xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2):
    '''
    >>> round(xy_diff_irr(0.011, 6, 0.011, 12, 0.1095/12, 6, irr_to_month_rate(12, 0.1095), 12), 5)
    0.07758
    >>> round(xy_diff_irr(0.16/12, 0, irr_to_month_rate(12, 0.16), 12, 0.1095/12, 0, irr_to_month_rate(12, 0.1095), 12), 5)
    0.05215
    '''
    pv = 10000
    plan = xy_diff_plan(pv, xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2)
    plan[0] = -pv
    for i in range(xnper2+1, len(plan)):
        plan[i] = plan[i] + pv*1.0 / ynper2
    return np.irr(plan) * 12


class XYInterest:
    def __init__(self, xrate, xnper, yrate, ynper):
        self.xrate = xrate
        self.yrate = yrate
        self.xnper = xnper
        self.ynper = ynper

class YPlans:
    '''
    >>> xy_intrerest1 = XYInterest(0, 0, 0.011, 12)
    >>> xy_intrerest2 = XYInterest(0.011, 6, 0.011, 12)
    >>> xy_intrerest3 = XYInterest(0.01, 6, 0.01, 12)
    >>> yp = YPlans()
    >>> mon = 0
    >>> yp.add2(mon, 2000000, 0, 0, 0.011, 12, 0.1095)
    >>> yp.add2(mon, 4000000, 0.011, 6, 0.011, 12, 0.1095)
    >>> yp.add2(mon, 4000000, 0.01, 6, 0.01, 12, 0.1095)
    >>> mon += 1
    >>> yp.add3(mon, 2000000, xy_intrerest1, 0.1095)
    >>> yp.add3(mon, 4000000, xy_intrerest2, 0.1095)
    >>> yp.add3(mon, 4000000, xy_intrerest3, 0.1095)
    >>> yp.add_batch(
    ...    (
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...        (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...        ((2000000, xy_intrerest1, 0.1095),
    ...         (4000000, xy_intrerest2, 0.1095),
    ...         (4000000, xy_intrerest3, 0.1095),),
    ...    ),
    ...    from_month_idx = 2
    ... )
    >>> #yp.month_plan
    >>> yp.principles
    [-10000000, -10000000, -10000000, -10000000, -10000000, -10000000, -10000000, -10000000, -10000000, -10000000, -10000000, -10000000]
    >>> #yp.revenues
    >>> yp.merge()
    >>> yp.merge_rev
    >>> yp.total_pv
    '''
    def __init__(self):
        self.month_plan = []
        self.principles = []
        self.yplans = []
        self.total_pv = []
        self.revenues = []
        self.merge_rev = None
        self.month_plan = defaultdict(list)
        self.principles = []

    def add(self, month_idx, total_pv, xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2):
        pre = np.array([0] * month_idx)

        self.month_plan[month_idx].append([total_pv, xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2])

        if len(self.principles) < month_idx+1:
            self.principles.append(0)
        self.principles[month_idx] = self.principles[month_idx] + (-total_pv)

        post = np.array(xy_diff_plan(total_pv, xrate1, xnper1, yrate1, ynper1, xrate2, xnper2, yrate2, ynper2))
        cash = np.concatenate([pre, post])
        self.revenues.append(cash)

        post = np.array(xy_yp_plan(total_pv, xrate1, xnper1, yrate1, ynper1))
        cash = np.concatenate([pre, post])
        self.yplans.append(cash)

    def add2(self, month_idx, total_pv, xrate1, xnper1, yrate1, ynper1, xy_irr_rate):
        return self.add(month_idx, total_pv, xrate1, xnper1, yrate1, ynper1,
            xy_irr_rate/12, xnper1, irr_to_month_rate(ynper1, xy_irr_rate), ynper1)

    def add3(self, month_idx, total_pv, xy_interest, xy_irr_rate):
        return self.add2(month_idx, total_pv,
            xy_interest.xrate, xy_interest.xnper, xy_interest.yrate, xy_interest.ynper,
            xy_irr_rate)

    def add_batch(self, plan_tuples, from_month_idx = 0):
        mon_idx = from_month_idx
        for plan in plan_tuples:
            for p in plan:
                self.add3(mon_idx, p[0], p[1], p[2])
            mon_idx += 1

    def merge(self):
        maxlen = max([len(r) for r in self.revenues])
        max_shape = (maxlen,)

        t = np.array([0]*maxlen)
        for r in self.revenues:
            x = r.copy()
            x.resize(max_shape)
            t = t + x
        self.merge_rev = t

        t = np.array([0]*maxlen)
        for r in self.yplans:
            x = r.copy()
            x.resize(max_shape)
            t = t + x
        merge_yplans = t

        totals = np.array(self.principles).copy()
        totals.resize(max_shape)
        self.total_pv = np.cumsum(totals + self.merge_rev + merge_yplans)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
