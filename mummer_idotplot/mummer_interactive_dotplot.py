#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import plotly.offline as offline
import plotly.graph_objs as go

def parse_mums(filename):
    ret = []
    query_store = None
    single_ref = False
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
        for l in reader:
            if l[0] == '>':  # start flag
                if l[-1] != 'Reverse':  # start line of match
                    if query_store:
                        ret.append(query_store)
                    query_store = {
                        'query_name': ' '.join(l[1:]),
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

def draw_map_plotly_multi(mums, refs, querys, single_ref, html=None):
    data = []
    refs_axes = ['x'+str(i+1) if i != 0 else 'x' for i in range(len(refs))]
    querys_axes = ['y'+str(i+1) if i != 0 else 'y' for i in range(len(querys))]
    for i in range(len(refs)):
        for j in range(len(querys)):
            for query_store in mums:
                if query_store['query_name'] == querys[j]:
                    for align in query_store['+']:
                        if single_ref or align[0] == refs[i]:
                            x = align[1]
                            y = align[2]
                            length = align[3]
                            data.append(go.Scattergl(x=[x,x+length], y=[y,y+length],
                                                     xaxis=refs_axes[i],
                                                     yaxis=querys_axes[j],
                                                     marker=dict(color='red')))
                    for align in query_store['-']:
                        if single_ref or align[0] == refs[i]:
                            x = align[1]
                            y = align[2]
                            length = align[3]
                            data.append(go.Scattergl(x=[x,x+length], y=[y+length,y],
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
            title=refs[i], domain=[start, end], showspikes=True, spikemode='across'
        )
        start += pitch
        end += pitch
    # querys
    pitch = 1 / len(querys)
    start, end = 0, pitch
    for j in range(len(querys)):
        option['yaxis' + str(j+1) if j != 0 else 'yaxis'] = dict(
            title=querys[j], domain=[start, end], showspikes=True, spikemode='across'
        )
        start += pitch
        end += pitch
    layout = go.Layout(option)
    fig = go.Figure(data=data, layout=layout)
    if html:
        offline.plot(fig, filename=html, auto_open=False)
    else:
        offline.iplot(fig)

