from bokeh.plotting import figure
from bokeh.embed import file_html,components
from bokeh.models import Legend,Range1d
from bokeh.models.formatters import DatetimeTickFormatter
import bokeh.palettes as palettes
from itertools import cycle,islice
import math
import numpy as np
from functools import update_wrapper
import datetime
import os
import time

# evil hack, because bokeh always renders UTC
os.environ['TZ'] = 'UTC+0'
time.tzset()

def make_label(s):
    rv = ""
    if s.name is None:
        rv = s.uid
    else:
        rv = s.name
        if not s.location is None:
            rv += " " + s.location
    return rv

def temp_over_datetime_plot(f):
    """ Decorator for temp vs. time plots """
    def new_func(*args, **kwargs):
        p = f(*args, **kwargs)
        p.axis.axis_label_text_font_size = '14pt'
        p.axis.major_label_text_font_size = '14pt'

        formatter = DatetimeTickFormatter()
        formatter.days = [ "%d.%m." ]
        p.xaxis.formatter = formatter
        p.xaxis.major_label_orientation = math.pi/4
        return p
    return update_wrapper(new_func, f)
        

@temp_over_datetime_plot
def temp_plot(labels, data):
    colors = list(islice(cycle(palettes.Set1[9]), len(data)))

    p = figure(
        #title='Temperaturverlauf letzte 7 Tage',
        x_axis_label='Datum und Zeit',
        x_axis_type='datetime',
        y_axis_label='Temperatur [Celsius]',
        plot_width=400,
        plot_height=400,
        responsive=True,
        active_drag=None,
        active_scroll=None,
        active_tap=None
    )

    curves = []
    for color,label,d in zip(colors, labels, data):
        xs = [ x.timestamp for x in d ]
        ys = [ x.temperature for x in d ]

        #p.line(xs, ys, legend=label, line_color=color)
        curves.append([p.line(xs, ys, line_color=color)])

        #print "tz: ", xs[0].tzname()
        #print "xs: ", xs
        #print "ys: ", ys

    legend = Legend(items=zip(labels,curves), location=(0,0))
    legend.label_text_font_size = '14pt'
    p.add_layout(legend, 'below')
    #p.legend.location = 'top_left'
    #p.legend.label_text_font_size = '14pt'

    return p

@temp_over_datetime_plot
def month_by_day(labels, data, date_range):
    colors = list(islice(cycle(palettes.Set1[9]), len(data)))

    p = figure(title='Monatsverlauf',
               x_axis_label='Datum und Zeit',
               x_axis_type='datetime',
               y_axis_label='Temperatur [Celsius]',
               plot_width=400,
               plot_height=400,
               responsive=True,
               active_drag=None,
               active_scroll=None,
               active_tap=None)

    curves = [] 
    min_temp = None
    max_temp = None
    for color,sensor_data in zip(colors,data):
        xs = []
        ys = []
        mins = []
        maxs = []
        for day_data in sensor_data:
            if not day_data.first() is None:
                xs.append(day_data.first().timestamp.replace(hour=12, minute=0, second=0))
                temps = [ x.temperature for x in day_data ]
                ys.append(np.mean(temps))
                mins.append(np.min(temps))
                maxs.append(np.max(temps))

        curves.append([p.patch(xs + list(reversed(xs)),
                               maxs + list(reversed(mins)),
                               alpha=0.3,
                               color=color),
                       p.circle(xs, ys, color=color),
                       p.line(xs, maxs, line_color=color),
                       p.line(xs, mins, line_color=color),
        ])

        if mins:
            if min_temp is None:
                min_temp = np.min(mins)
            else:
                min_temp = np.min(mins + [min_temp])

        if maxs:
            if max_temp is None:
                max_temp = np.max(maxs)
            else:
                max_temp = np.max(maxs + [max_temp])

    p.x_range = Range1d(date_range[0], date_range[1])
    p.xaxis.bounds = date_range
    if not min_temp is None and not max_temp is None:
        p.yaxis.bounds = (min_temp, max_temp)

    legend = Legend(items=zip(labels,curves), location=(0,0))
    legend.label_text_font_size = '14pt'
    p.add_layout(legend, 'below')

    return p

@temp_over_datetime_plot
def year_by_month(labels, data, date_range):
    colors = list(islice(cycle(palettes.Set1[9]), len(data)))

    p = figure(title='Jahresverlauf',
               x_axis_label='Datum und Zeit',
               x_axis_type='datetime',
               y_axis_label='Temperatur [Celsius]',
               plot_width=400,
               plot_height=400,
               responsive=True,
               active_drag=None,
               active_scroll=None,
               active_tap=None)

    curves = [] 
    min_temp = None
    max_temp = None
    for color,sensor_data in zip(colors,data):
        xs = []
        ys = []
        mins = []
        maxs = []
        for month_data in sensor_data:
            if not month_data.first() is None:
                xs.append(month_data.first().timestamp.replace(day=15, hour=12, minute=0, second=0))
                temps = [ x.temperature for x in month_data ]
                ys.append(np.mean(temps))
                mins.append(np.min(temps))
                maxs.append(np.max(temps))

        curves.append([p.patch(xs + list(reversed(xs)),
                               maxs + list(reversed(mins)),
                               alpha=0.3,
                               color=color),
                       p.circle(xs, ys, color=color),
                       p.line(xs, maxs, line_color=color),
                       p.line(xs, mins, line_color=color),
        ])

        if mins:
            if min_temp is None:
                min_temp = np.min(mins)
            else:
                min_temp = np.min(mins + [min_temp])

        if maxs:
            if max_temp is None:
                max_temp = np.max(maxs)
            else:
                max_temp = np.max(maxs + [max_temp])

    p.x_range = Range1d(date_range[0], date_range[1])
    p.xaxis.bounds = date_range
    if not min_temp is None and not max_temp is None:
        p.yaxis.bounds = (min_temp, max_temp)

    legend = Legend(items=zip(labels,curves), location=(0,0))
    legend.label_text_font_size = '14pt'
    p.add_layout(legend, 'below')

    return p
