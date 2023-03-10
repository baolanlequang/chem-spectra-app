from chem_spectra.lib.shared.calc import *

# def test_calc_j():
#     #TODO: implement later
#     pass

def test_calc_ks():
    ys = np.array([1.0, 2.0, 3.0, 4.0])
    y_max = 3.0
    h = 3.0
    ks = calc_ks(ys, y_max, h)
    assert np.alltrue(ks == [0.01, 0.03, 0.06, 0.1])

def test_centerX_no_values():
    ps = []
    center_x = centerX(ps=ps, shift=0)
    assert center_x == 0.0

def test_centerX_odd_number_values():
    ps = [{'x':1.0}, {'x':2.0}, {'x':3.0}]
    center_x = centerX(ps=ps, shift=0)
    assert center_x == 2.0

def test_centerX_even_number_values():
    ps = [{'x':1.0}, {'x':2.0}, {'x':3.0}, {'x':4.0}]
    center_x = centerX(ps=ps, shift=0)
    assert center_x == 2.0

def test_centerX_with_shift():
    ps = [{'x':1.0}, {'x':2.0}, {'x':3.0}, {'x':4.0}]
    center_x = centerX(ps=ps, shift=0.5)
    assert center_x == 1.5

def test_calc_mpy_center_not_t_typ():
    ps = [{'x':1.0}, {'x':2.0}, {'x':3.0}, {'x':4.0}]
    mpy_typ = ['s', 'd', 'm']
    for typ in mpy_typ:    
        center_x = calc_mpy_center(ps=ps, shift=0, typ=typ)
        assert center_x == 2.5

def test_calc_mpy_center_t_typ():
    ps = [{'x':1.0}, {'x':2.0}, {'x':3.0}, {'x':4.0}]
    center_x = calc_mpy_center(ps=ps, shift=0, typ='t')
    assert center_x == 2.5

def test_calc_mpy_center_t_typ_three_values():
    ps = [{'x':1.0}, {'x':2.0}, {'x':4.0}]
    center_x = calc_mpy_center(ps=ps, shift=0, typ='t')
    assert center_x == 2.0

def test_get_curve_endpoint():
    #TODO: implement later
    pass

def test_to_float_with_int_value():
    float_value = to_float(10)
    assert type(float_value) is float
    assert float_value == 10.0

def test_to_float_with_float_value():
    float_value = to_float(10.0)
    assert type(float_value) is float
    assert float_value == 10.0

def test_to_float_with_string_value_with_dot():
    float_value = to_float('10.2')
    assert type(float_value) is float
    assert float_value == 10.2

def test_to_float_with_string_value_with_comma():
    float_value = to_float('10,2')
    assert type(float_value) is float
    assert float_value == 10.2

def test_cal_slope_no_slope():
    slope_1 = cal_slope(x1=1.0, x2=1.0, y1=1.0, y2=2.0)
    assert slope_1 == 0
    slope_2 = cal_slope(x1=1.0, x2=2.0, y1=1.0, y2=1.0)
    assert slope_2 == 0

def test_cal_slope():
    slope = cal_slope(x1=1.0, x2=2.0, y1=1.0, y2=2.0)
    assert slope == 1.0

def test_cal_xyIntegration_wrong_value():
    xs = [1.0, 2.0, 3.0]
    ys = [1.0, 2.0, 3.0, 4.0]
    integration_value = cal_xyIntegration(xs=xs, ys=ys)
    assert integration_value == 0

def test_cal_xyIntegration():
    xs = [1.0, 2.0, 3.0]
    ys = [1.0, 2.0, 3.0]
    integration_value = cal_xyIntegration(xs=xs, ys=ys)
    assert integration_value == 4.0

def test_cal_area_multiplicity():
    xL = 1.0
    xU = 2.0
    data_xs = [1.0, 2.0]
    data_ys = [2.0, 4.0]
    area = cal_area_multiplicity(xL, xU, data_xs=data_xs, data_ys=data_ys)
    assert area == 1.0
