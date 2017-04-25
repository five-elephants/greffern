from bokeh.plotting import figure
from bokeh.embed import file_html,components
from bokeh.models import Legend
from bokeh.models.formatters import DatetimeTickFormatter
import bokeh.palettes as palettes
from itertools import cycle,islice
import math

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

    legend = Legend(items=zip(labels,curves), location=(0,0))
    legend.label_text_font_size = '14pt'
    p.add_layout(legend, 'below')
    #p.legend.location = 'top_left'
    #p.legend.label_text_font_size = '14pt'

    p.axis.axis_label_text_font_size = '14pt'
    p.axis.major_label_text_font_size = '14pt'

    formatter = DatetimeTickFormatter()
    formatter.days = [ "%d.%m." ]
    p.xaxis.formatter = formatter
    p.xaxis.major_label_orientation = math.pi/4


    return components(p)
