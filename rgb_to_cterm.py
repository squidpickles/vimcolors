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

	def update_color_line(self, line):
		if not line.startswith("hi"):
			return line
		if not 'gui' in line:
			return line
		settings = dict()
		parts = line.split(' ')
		for part in parts[2:]:
			if '=' not in part:
				continue
			key, value = part.split('=')
			settings[key] = value
		for key in [key for key in settings.keys() if key.startswith('gui')]:
			value = settings[key]
			cterm_key = key.replace('gui', 'cterm')
			if value.startswith('#'):
				cterm_value = self.find_nearest(value[1:])
			else:
				cterm_value = value
			settings[cterm_key] = cterm_value
		new_settings = " ".join(["=".join((k, str(settings[k]))) for k in reversed(sorted(settings.keys()))])
		new_line = "{} {} {}".format(parts[0], parts[1], new_settings)
		return new_line

def main():
	tester = ColorTester('colors.tsv')
	with open("/home/sweetpea/.vim/colors/mine.vim", "r") as mine:
		for line in mine:
			print(tester.update_color_line(line.rstrip()))

if __name__ == '__main__':
	main()
