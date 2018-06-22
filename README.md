# vimcolors

Vim GUI to cterm color converter

It's pretty slow -- it was a quick hack to make a nice color scheme one afternoon, and it brute-forces its way to matches.

## Usage

```python
>>> from rgb_to_cterm import ColorTester

>>> tester = ColorTester('colors.tsv')  # colors.tsv is the list of mappings from hex to cterm
>>> tester.find_nearest('d700d7')
164
```

Or you can take a sample vim color file:

```python
>>> from rgb_to_cterm import ColorTester

>>> tester = ColorTester('colors.tsv')  # colors.tsv is the list of mappings from hex to cterm
>>> with open('colors.vim') as colors:
...     for line in colors:
...         print(tester.update_color_line(line.rstrip()))
hi Normal guifg=#000000 guibg=#ffffff gui=NONE ctermfg=0 ctermbg=15 cterm=NONE
hi Comment guifg=#808080 guibg=NONE gui=italic ctermfg=8 ctermbg=NONE cterm=italic
hi Constant guifg=#3a6f05 guibg=NONE gui=NONE ctermfg=2 ctermbg=NONE cterm=NONE
hi Directory guifg=#3a6f05 guibg=NONE gui=NONE ctermfg=2 ctermbg=NONE cterm=NONE
hi Identifier guifg=#67007c guibg=NONE gui=NONE ctermfg=54 ctermbg=NONE cterm=NONE
[...]
```
