import matplotlib.pyplot as plt
import numpy as np

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def live_plotter(x_vec,y1_data,y2_data,line1,line2,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, 'r-o', alpha=0.8, label='Trump')
        line2, = ax.plot(x_vec, y2_data, 'b-o', alpha=0.8, label='Biden')
        #update plot label/title
        plt.ylabel('Sentiment')
        plt.title('Trump vs Biden'.format(identifier))
        ax.legend(loc='upper center', shadow=True, fontsize='x-large')
        textstr = '\n'.join((
            r'$\Trump Average: %.2f$' % (np.average(y1_data),),
            r'$\Biden Average: %.2f$' % (np.average(y2_data),)))
        ax.text(0, 0.95, textstr, fontsize='x-large', horizontalalignment='left',
                verticalalignment='top')  # , bbox=props)
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    line2.set_ydata(y2_data)
    # adjust limits if new data goes beyond bounds
    plt.ylim([-1, 1])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1, line2

# the function below is for updating both x and y values (great for updating dates on the x-axis)
def live_plotter_xy(x_vec,y1_data,y2_data,line1,line2,identifier='',pause_time=0.01):
    if line1==[]:
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        line1, = ax.plot(x_vec,y1_data,'r-o',alpha=0.8,  label='Trump')
        line2, = ax.plot(x_vec,y2_data,'b-o', alpha=0.8, label='Biden')
        plt.ylabel('Sentiment')
        plt.title('Trump vs Biden'.format(identifier))
        ax.legend(loc='upper center', shadow=True, fontsize='x-large')
        textstr = '\n'.join((
            r'$\Trump Average: %.2f$' % (np.average(y1_data),),
            r'$\Biden Average: %.2f$' % (np.average(y2_data),)))
        ax.text(0, 0.95, textstr, fontsize='x-large', horizontalalignment='left',
                verticalalignment='top')#, bbox=props)
        plt.show()
        
    line1.set_data(x_vec,y1_data)
    line2.set_data(x_vec,y2_data)
    plt.xlim(np.min(x_vec),np.max(x_vec))
    plt.ylim([-1, 1])
    plt.pause(pause_time)
    
    return line1, line2
