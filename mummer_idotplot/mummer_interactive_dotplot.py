#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import plotly.offline as offline
import plotly.graph_objs as go

import matplotlib.pyplot as plt
import matplotlib.collections as mc

def parse_mums(filename):
    ret = []
    query_store = None
    single_ref = False
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
        for l in reader:
            if l[0] == '>':  # start flag
                length = int(' '.join(l[1:]).split('\t')[-1].split(' ')[-1])
                name_with_flag = ''.join(' '.join(l[1:]).split('\t')[:-1])
                L = name_with_flag.split(' ')
                if L[-1] != 'Reverse':  # start line of match
                    if query_store:
                        ret.append(query_store)
                    query_store = {
                        'query_name': ' '.join(L),
                        'length': length,
                        '+': [],
                        '-': []
                    }
                    direction = '+'
                else:  # reverse match is reported after forward match
                    direction = '-'
            else:
                if len(l) > 3:
                    # (ref_id, refでの開始位置, queryでの開始位置, match length)
                    query_store[direction].append((l[0], int(l[1]), int(l[2]), int(l[3])))
                    single_ref = False
                else:
                    # (ref_id = 'query', refでの開始位置, queryでの開始位置, match length)
                    query_store[direction].append(('reference', int(l[0]), int(l[1]), int(l[2])))
                    single_ref = True
        ret.append(query_store)
    return ret, single_ref

def is_in_region(xl, xr, bl, br):
    cond = True
    if bl:
        cond = cond and bl <= xr
    if br:
        cond = cond and xl <= br
    return cond

def draw_map_matplotlib(ax, mums, ref, query, single_ref):
    lines_f, lines_b = [], []
    for query_store in mums:
        if query_store['query_name'] == query[0]:
            query_length = query_store['length']
            for align in query_store['+']:
                if single_ref or align[0] == ref[0]:
                    x = align[1]
                    y = align[2]
                    length = align[3]
                    xl, xr = x, x + length
                    yl, yr = y, y + length
                    if is_in_region(xl, xr, ref[1], ref[2]) and is_in_region(yl, yr, query[1], query[2]):
                        lines_f.append(((xl, yl), (xr, yr)))
            for align in query_store['-']:
                if single_ref or align[0] == ref[0]:
                    x = align[1]
                    y = align[2]
                    length = align[3]
                    xl, xr = x, x + length
                    yl, yr = query_length - y, query_length - y - length
                    if is_in_region(xl, xr, ref[1], ref[2]) and is_in_region(yr, yl, query[1], query[2]):
                        lines_b.append(((xl, yl), (xr, yr)))
    lc_f = mc.LineCollection(lines_f, color='red', linewidths=1)
    lc_b = mc.LineCollection(lines_b, color='blue', linewidths=1)
    ax.add_collection(lc_f)
    ax.add_collection(lc_b)
    ax.set_xlabel(ref[0])
    ax.set_ylabel(query[0])
    ax.ticklabel_format(style='sci',axis='both',scilimits=(0,0))
    if (ref[1] is None or ref[2] is None or query[1] is None or query[2] is None):
        ax.autoscale()
    else:
        ax.set_xlim(ref[1], ref[2])
        ax.set_ylim(query[1], query[2])
    ax.grid(which='major')
    ax.set_aspect('equal')

def draw_map_plotly_multi(mums, refs, querys, single_ref, html=None):
    data = []
    refs_axes = ['x'+str(i+1) if i != 0 else 'x' for i in range(len(refs))]
    querys_axes = ['y'+str(i+1) if i != 0 else 'y' for i in range(len(querys))]
    for i in range(len(refs)):
        for j in range(len(querys)):
            for query_store in mums:
                if query_store['query_name'] == querys[j][0]:
                    query_length = query_store['length']
                    for align in query_store['+']:
                        if single_ref or align[0] == refs[i][0]:
                            x = align[1]
                            y = align[2]
                            length = align[3]
                            xl, xr = x, x + length
                            yl, yr = y, y + length
                            if is_in_region(xl, xr, refs[i][1], refs[i][2]) and is_in_region(yl, yr, querys[j][1], querys[j][2]):
                                data.append(go.Scattergl(x=[xl, xr], y=[yl, yr],
                                                         xaxis=refs_axes[i],
                                                         yaxis=querys_axes[j],
                                                         marker=dict(color='red')))
                    for align in query_store['-']:
                        if single_ref or align[0] == refs[i][0]:
                            x = align[1]
                            y = align[2]
                            length = align[3]
                            xl, xr = x, x + length
                            yl, yr = query_length - y, query_length - y - length
                            if is_in_region(xl, xr, refs[i][1], refs[i][2]) and is_in_region(yr, yl, querys[j][1], querys[j][2]):
                                data.append(go.Scattergl(x=[xl, xr], y=[yl, yr],
                                                         xaxis=refs_axes[i],
                                                         yaxis=querys_axes[j],
                                                         marker=dict(color='blue')))
    # output
    option = dict(showlegend=False, barmode='stack')
    # references
    pitch = 1 / len(refs)
    start, end = 0, pitch
    for i in range(len(refs)):
        option['xaxis' + str(i+1) if i != 0 else 'xaxis'] = dict(
            title=refs[i][0], domain=[start, end], showspikes=True, spikemode='across'
        )
        start += pitch
        end += pitch
    # querys
    pitch = 1 / len(querys)
    start, end = 0, pitch
    for j in range(len(querys)):
        option['yaxis' + str(j+1) if j != 0 else 'yaxis'] = dict(
            title=querys[j][0], domain=[start, end], showspikes=True, spikemode='across'
        )
        start += pitch
        end += pitch
    layout = go.Layout(option)
    fig = go.Figure(data=data, layout=layout)
    if html:
        offline.plot(fig, filename=html, auto_open=False)
    else:
        offline.iplot(fig)

