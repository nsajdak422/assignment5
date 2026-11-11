'''
Title: Assignment5
Author: Nathan Sajdak
Date: 03 November 2026
'''

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

#Global variables
A = 10 #V/m
a = 2 #m
k = 0.4 #1/m
xlow = 0
xhigh = 20
pi = np.pi


#Question 1
dx = 0.1 #step size
x = np.arange(xlow, xhigh + dx, dx)
E_x = A * np.cos(pi * x / a) * np.exp(-k * x)
    
#plot 
plt.figure()
plt.plot(x,E_x)
plt.xlabel('Waveguide x (m)')
plt.ylabel('E_Field (V/m)')
plt.title('Electric Field along Waveguide')



#Question 2
def dx_waveguide(step, meth):
    E_x_posh = A * np.cos(pi * (x + step) / a) * np.exp(-k * (x + step))
    E_x_negh = A * np.cos(pi * (x - step) / a) * np.exp(-k * (x - step))
    
    if meth == 1:  #Forward Differencing
        return (E_x_posh - E_x) / step
    elif meth == 2:  #Central Differencing
        return (E_x_posh - E_x_negh) / 2 / step
    elif meth == 3: #Analytic Derivative
        return -A * np.exp(-k*x) * (pi/a * np.sin(pi*x/a) + k*np.cos(pi*x/a))   
        
    
def figures(step):
    e_x_forward = dx_waveguide(step, 1)
    e_x_central = dx_waveguide(step, 2)
    e_x_analytical = dx_waveguide(step, 3)

    plt.figure()
    plt.plot(x, e_x_forward, label='Forward', color='blue')
    plt.plot(x, e_x_central, label='Central', color='red')
    plt.plot(x, e_x_analytical, label='Analytical', color='green')
    plt.xlabel('Waveguide x (m)')
    plt.ylabel('E_Field (V/m)')
    plt.title('Electric Field Change along Waveguide; Multiple Methods; dx={}'.format(step))
    plt.legend()
    
    error_forward = np.abs(e_x_analytical - e_x_forward)
    error_central = np.abs(e_x_analytical - e_x_central)
    
    plt.figure()
    plt.yscale('log')
    plt.plot(x, error_forward, label='Forward E.', color='blue')
    plt.plot(x, error_central, label='Central E.', color='red')
    plt.xlabel('Waveguide x (m)')
    plt.ylabel('Error Num vs. Anly (V/m)')
    plt.title('Error between Analytic and Numerical Analysis; Multiple Methods; dx={}'.format(step))
    plt.legend()
    
    
 
#2C/D    
figures(0.1)
#The Central Differencing method is significantly more accurate, especially at
#lower x values. As the x value increases, both methods became near perfect.


#2E
figures(0.05)
#With the step sized halved, the error appeared to decrease by about half as
#well. This is because we have reduced the truncation error by an equal amount,
#increasing the step size to allow so. This makes this first-order
#approximation more accurate.


#2F
step_array = np.logspace(-1, -15, num=15)
E_x_1 = A * np.cos(pi * 1 / a) * np.exp(-k * 1)
E_x_posh_1 = A * np.cos(pi * (1 + step_array) / a) * np.exp(-k * (1 + step_array))
e_x_forward_1 = (E_x_posh_1 - E_x_1) / step_array
e_x_analytical_1 = -A * np.exp(-k*1) * (pi/a * np.sin(pi*1/a) + k*np.cos(pi*1/a))

plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.plot(step_array, np.abs(e_x_analytical_1 - e_x_forward_1))
plt.xlabel('Step Size (m)')
plt.ylabel('Analytical vs. Forward Error (V/m)')
plt.title('Analytical vs. Forward Diff. Error Over Decreasing Step Sizes')
#This error eventually increases most likely due to rounding error in the
#Python algorithms (floating point precision issues).



#Question 3
data = pd.read_csv('fismflux20020824.dat', comment='#', sep='\s+', header=None)

#Making the a set of realtime data for the x-axis
columns_mapping = {
    0: 'year', 
    1: 'month', 
    2: 'day', 
    3: 'hour', 
    4: 'minute', 
    5: 'second'
    } 
data['time'] = pd.to_datetime(data[[0,1,2,3,4,5]].rename(columns=columns_mapping))

#y-axis
bin_56 = data[6 + 55]

#plot
plt.figure()
plt.plot(data['time'], bin_56)
plt.xlabel('Time (2002-08-24) (HH:MM)')
plt.ylabel('56th Bin of EUV Spectrum (W/m^2/nm)')
plt.title('56th Bin of EUV Spectrum vs. Real Time')
plt.gcf().autofmt_xdate() #rotates the time data
#Formats the X-axis to only show HH:MM of the RealTime data
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))






