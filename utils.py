import numpy as np 
import matplotlib.pyplot as plt
import datetime

def plot_totals(cases,deaths=None):
    epochs = range(1,len(cases)+1)
    _, ax = plt.subplots()
    # ax.plot(xline, means_smooth, lw=1, color= '#539caf', alpha = 1, label= 'mean')
    # ax.fill_between(xline,mins_smooth,maxes_smooth,color='orange',alpha = 0.4, label = 'Min/Max')

    ax.plot(epochs,cases,'g',label="Confirmed Cases")
    if deaths:
        ax.plot(epochs,deaths,'m',label="Deaths")
    ax.set_title('Covid19')
    ax.set_xlabel('Days')
    ax.set_ylabel('Cases')
    ax.legend()
    plt.show()
    # plt.savefig('assets/Covid19',bbox_inches='tight')
    # plt.close()

def unwrap_projections(projections):
    data = [[] for _ in range(len(projections[0]))]
    for projection in projections:
        for i,d in enumerate(projection):
            data[i].append(d)
    return data

def return_polyfit(x,y,degree):
    import numpy.polynomial.polynomial as poly
    coefs = poly.polyfit(x, y, degree)
    ffit = poly.polyval(x, coefs)
    return ffit,coefs

def parse_date(date_str):
    return datetime.datetime.strptime(date_str,'%m/%d/%y')

def determine_R0(points):
    """
    Requires two data points (x,y)
    first X is assumed to be 0
    Ae^rx = y
    """
    x1,y1 = points[0]
    x2,y2 = points[1]
    R0 = np.power((y2/y1),(1/(x2-x1)))
    A = y1 / np.power(R0,x1)
    return R0,A

def graph_expo(x,points):
    x1,y1 = points[0]
    x2,y2 = points[1]
    y = y1 * np.power((y2/y1),(x-x1 / x2-x1))
    return y 

def decay_to_max(max_daily,last_point,duration):
    points = []
    new_point = last_point + ((max_daily - last_point) / 2)
    print('last_point',last_point,'new_point',new_point)
    for _ in range(duration):
        points.append(new_point)
        new_point += (max_daily - new_point) / 2
    return np.array(points)