from absl import app
import pandas as pd
import json
import svgwrite
from svglib.svglib import svg2rlg
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF


def main(argv):
    print("Plot Test")
    print('https://pythonfix.com/code/svgwrite_code_examples/')

    palette_red = ['#5c1d3d', '#932e47', '#c54a42', '#eb7331', '#ffa600']
    palette_green = ['#1c5c12', '#4e7c15', '#839b18', '#beba21', '#ffd633']
    palette_blue = ['#104a5c', '#2a6d83', '#4393ab', '#5dbbd4', '#78e4ff']

    data = {
        'bars': [
            {
                'min': 0,
                'max': 100,
                'name': 'gender',
                'labels': ['f', 'm', 'd'],
                'values': [40,40,20],
                'colors': palette_green,
                'legend': ['female', 'male', 'diverse']
            },
            {
                'min': 0,
                'max': 100,
                'name': 'cultural$background',
                'labels': ['FR', 'DE', '', ''],
                'values': [10,80,8,2],
                'colors': palette_blue,
                'legend': ['France', 'Germany', 'USA', 'Spain']
            },
            {
                'min': 0,
                'max': 100,
                'name': 'music$perception',
                'labels': ['low', '', '', '', 'high'],
                'values': [20,30,10,20,20],
                'colors': palette_red,
                'legend': ['low', '', '', '', 'high']
            }
        ]
    }
    plot_bar_chart('../plots/test.svg', '../plots/test.pdf', width=520, height=330, data=data, title='Participants')


def plot_bar_chart(path_svg, path_pdf, width, height, data, title=''):

    # -- settings --------
    fs_header = 28
    fs_axis = 12
    fs_label = 16
    fs_value = 10
    fs_legend = 10
    font =  'Verdana'
    fontBold = 'Verdana-Bold'
    colorTitle = '#333'
    colorAxis = '#333'
    colorLabel = '#f0f0f0'
    colorValue = '#f0f0f0'
    colorLegend = '#666'
    showValue = False
    valueInPercent = True
    paddingY = 10
    bar_x = 100
    bar_w = 400
    bar_h = 48
    bar_p = 8

    # -- draw --------
    dwg = svgwrite.Drawing(path_svg, size=(width, height), profile='full')

    # background
    dwg.add(dwg.rect((0, 0), (width, height), fill='#fafafa'))

    # title
    x = 0
    y = paddingY
    if title != '':
        y += fs_header
        header = dwg.text(title,
                        insert=(bar_x, y),
                        stroke='none',
                        fill=colorTitle,
                        text_anchor='start',
                        font_size='{}px'.format(fs_header),
                        font_family=fontBold)
        dwg.add(header)
        y += 20

    # draw bars below each other
    bars = data['bars']
    clip_path_id = f'bar_mask'
    clip_path = dwg.defs.add(dwg.clipPath(id=clip_path_id))
    clip_path.add(dwg.rect((0, 0), (bar_w, bar_h), rx=3, ry=3, fill='#000000'))

    for i, bar in enumerate(bars):
        # add a new group for each bar: 1.y-label |  2.bar   |
        g_bar = dwg.g()
        g_bar.translate(x, y)
        dwg.add(g_bar)
        bar_y = i * (bar_h+bar_p)

        # 1. draw y-axis label
        # y_label = dwg.text(bar['name'],
        #                 insert=(bar_x-8, bar_y+bar_h/2+fs_y_axis/2),
        #                 stroke='none',
        #                 fill='#333',
        #                 text_anchor='end',
        #                 font_size='{}px'.format(fs_y_axis),
        #                 font_family=fontBold)
        y_label = multi_line(dwg,
            x=bar_x-8,
            y=(bar_y+bar_h/2-fs_axis/2),
            text=bar['name'],
            font_size=fs_axis,
            line_height=fs_axis,
            line_length=100,
            h_align='end',
            v_align='center',
            color=colorAxis,
            font_family=fontBold)
        g_bar.add(y_label)

        # 2. draw stacked bar
        g_barstack = dwg.g()
        g_bar.add(g_barstack)
        g_barstack.translate(bar_x, bar_y)

        # bg (with x offset to ll)
        bg = dwg.rect((0, 0), (bar_w, bar_h), rx=0, ry=0, fill='#f1f1f1', clip_path=f"url(#{clip_path_id})")
        g_barstack.add(bg)

        # draw horizontal stacks | 0 |   1   | 2 |
        val_min = bar['min']
        val_max = bar['max']
        stack_x = 0
        for j, val in enumerate(bar['values']):
            # calculate the width of a stack part, based on its value
            val_percent =  (val-val_min)/(val_max-val_min)
            if val_percent > 0:
                lb = bar['labels'][j]
                stack_w = val_percent * bar_w
                color = bar['colors'][j]
                stack = dwg.rect((stack_x, 0), (stack_w, bar_h), rx=0, ry=0, fill=color, clip_path=f"url(#{clip_path_id})")
                g_barstack.add(stack)

                # add huge center label
                if lb != '':
                    lb_x = stack_x + stack_w/2
                    lb_y = bar_h/2 + fs_label/2-2
                    label = dwg.text(lb,
                                    insert=(lb_x, lb_y),
                                    stroke='none',
                                    fill=colorLabel,
                                    text_anchor='middle',
                                    font_size='{}px'.format(fs_label),
                                    font_family=fontBold)
                    g_barstack.add(label)

                # add label thats shows the value
                if showValue:
                    lb_x = stack_x + stack_w/2 #stack_x + stack_w - 3
                    lb_y = bar_h-4#3 + fs_value
                    lb_val = '{:.0f}%'.format(val_percent*100) if valueInPercent else f'{val}'
                    label = dwg.text(lb_val,
                                    insert=(lb_x, lb_y),
                                    stroke='none',
                                    fill=colorValue,
                                    text_anchor='middle',
                                    font_size='{}px'.format(fs_value),
                                    font_family=font)
                    g_barstack.add(label)

                # increase x for next stack part
                stack_x += stack_w

    # draw legend
    g_legend = dwg.g()
    y += (len(bars) * bar_h+bar_p) + 30
    g_legend.translate(bar_x, y)
    #g_legend.translate(30, y)
    #g_legend.translate(bar_x + bar_w + 40, paddingY + 20 + fs_header)
    legend_h = 12
    legend_p = 4
    dwg.add(g_legend)
    row_x = 0
    row_y = 0
    for i, bar in enumerate(bars):
        for j, val in enumerate(bar['values']):
            if 'legend' in bar:
                g_l = dwg.g()
                g_l.translate(row_x, row_y)
                g_legend.add(g_l)

                # rectangle
                color = bar['colors'][j]
                rect = dwg.rect((0, 0), (legend_h, legend_h), rx=3, ry=3, fill=color)
                g_l.add(rect)

                # label
                lb_legend = bar['legend'][j] if len(bar['legend']) >= j-1 else '--'
                lb_x = legend_h + 4
                lb_y = legend_h/2 + fs_legend/2 - 1
                lb_val = 'some legend text'
                label = dwg.text(lb_legend,
                                insert=(lb_x, lb_y),
                                stroke='none',
                                fill=colorLegend,
                                text_anchor='start',
                                font_size='{}px'.format(fs_legend),
                                font_family=font)
                g_l.add(label)

                row_y += (legend_h+legend_p)
        row_y = 0
        row_x += 100


    # -- store --------
    dwg.embed_font('Verdana', '../assets/fonts/Verdana.ttf')
    dwg.embed_font('Verdana-Bold', '../assets/fonts/Verdana Bold.ttf')
    dwg.save()
    print('Saved {}'.format(path_svg))

    # svg to pdf
    pdfmetrics.registerFont(TTFont('Verdana-Bold', '../assets/fonts/Verdana Bold.ttf'))
    f = svg2rlg(path_svg)
    renderPDF.drawToFile(f, path_pdf)
    print('Saved {}'.format(path_pdf))


def multi_line(dwg, x, y, text, font_size, line_height, line_length, h_align='start', v_align='start', color='#333', font_family='Verdana'):

    # line break on line length (but only between words) OR on special char $
    lines = []
    br = '$'
    line = ''
    cnt = 0
    num = len(text)
    for i, c in enumerate(text):
        if c != br:
            line += c
        if (0 < line_length < cnt and c == ' ') or i >= num - 1 or c == br:
            lines.append(line)
            line = ''
            cnt = 0
        cnt += 1

    # calc y based on vertical align (ignore first line)
    # soooo position in general is based on top-left text corner (or top-right if h_align = end)
    h = line_height * len(lines) - line_height
    if v_align == 'end':
        y = y - h
    elif v_align == 'middle' or v_align == 'center':
        y = y - h/2

    # create svg from multiple lines
    p = dwg.text('', x=[x], y=[y], stroke='none', fill=color, text_anchor=h_align,
                 font_size='{}px'.format(font_size), font_family=font_family)
    for l in lines:
        tspan = dwg.tspan(l, x=[x], dy=[line_height], text_anchor=h_align)
        p.add(tspan)


    return p


if __name__ == "__main__":
    app.run(main)