import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from matplotlib import rc as pRC
import numpy as np 

import datetime as dt

from io import BytesIO

# graph choices
G_CHOICES = ['cases', 'deaths', 'recovered', 'all']
COLOURS = ['lightblue', 'red', 'lightgreen']


class Graph:
	""" graphing class for plotting the covid data, 
	takes a timeline dict as argument"""

	def __init__(self, timeline, log=False):
		dates, cases, deaths, recovered = [], [], [], []
		for k, v in timeline.items():
			dates.append(k)
			cases.append(v['cases'])
			deaths.append(v['deaths'])
			recovered.append(v['recovered'])

		self.dates = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
		self.y = np.array([cases, deaths, recovered])
		self.fig, self.ax = self._format_axis()

		if log:
			self.ax.set_yscale('log')
			plt.minorticks_off()

	def _plot_data(self, index, fill=True, **kwargs):
		""" plots data from self.y according to the index; appends kwargs to the fmt options
		of plt.plot """
		formatting = {
			'label'		:	G_CHOICES[index], 
			'c'			:	COLOURS[index],
			'marker'	: 	'o',
			'ms'		:   2,
			**kwargs
		}
		self.ax.plot(self.dates, self.y[index], **formatting)
		if fill:
			self.ax.fill_between(self.dates, self.y[index], alpha=0.5, color=formatting['c'])

	def _format_axis(self):
		""" formats the axis properly """
		fig = plt.figure(dpi=150)
		ax = plt.gca()

		#plt.style.use('dark_background')

		ax.yaxis.grid()
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
		ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))

		# get rid of the spines
		for loc in ['top', 'right', 'left']:
			ax.spines[loc].set_visible(False)

		return fig, ax

	def plot_all(self):
		""" plots cases, deaths, and recovered """
		for i in range(3):
			self._plot_data(i)

	def save(self):
		""" save the figure and return bytes """
		self.fig.autofmt_xdate()
		self.ax.legend(loc='upper left', fancybox=True, facecolor='0.2')

		# write image to buffer
		pRC('savefig', format='png')
		buf = BytesIO()
		plt.savefig(buf)
		buf.seek(0)

		# tear down
		self.fig.clf()
		plt.close(self.fig)

		return buf
