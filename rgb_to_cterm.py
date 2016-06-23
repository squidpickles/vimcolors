from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color

import csv
import re

def build_color(hex_string):
		rr, gg, bb = re.findall('..', hex_string)
		rgb = sRGBColor(int(rr, 16), int(gg, 16), int(bb, 16), True)
		return convert_color(rgb, LabColor)

class ColorTester(object):
	def __init__(self, color_filename):
		self._term_colors = dict()
		self._hex_colors = dict()
		self._load_color_list(color_filename)

	def _load_color_list(self, color_filename):
		with open(color_filename, 'r') as color_file:
			reader = csv.reader(color_file, delimiter='\t')
			for line in reader:
				term_color = int(line[1])
				color = build_color(line[0])
				self._term_colors[color] = term_color
				self._hex_colors[line[0]] = term_color

	def find_nearest(self, candidate):
		if candidate in self._hex_colors:
			return self._hex_colors[candidate]
		candidate_color = build_color(candidate)
		closest = None
		min_delta = 9999999999
		for color, term_color in self._term_colors.items():
			delta = abs(delta_e_cie2000(color, candidate_color))
			if delta < min_delta:
				closest = term_color
				min_delta = delta
		self._hex_colors[candidate] = closest # cache for next time
		return closest

def main():
	tester = ColorTester('colors.tsv')
	to_test = ("875f87", "87005f", "0000d7", "d700d7", "00ff00", "ffffff", "00afaf", "afff01", "afd600", "afff01")
	for candidate in to_test:
		print(tester.find_nearest(candidate))

if __name__ == '__main__':
	main()
