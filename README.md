
# Nitram Micro Mono

A custom pixel based font which only needs 5x5 pixel per character.
I've used it in some older projects, back in the MS-DOS days ...
Remember when your screen resolution was only 320x200 pixel in total ;-)

![Sample: The quick brown fox jumps over the lazy dog](/the_quick_brown_fox_jumps_over_the_lazy_dog.png?raw=true)

It's source is in [CP437](https://en.wikipedia.org/wiki/Code_page_437)
code page and suitable for drawing [ASCII art](https://en.wikipedia.org/wiki/ASCII_art) ;-)

![Sample: all characters](/sample.png?raw=true)

## License

[MIT](https://opensource.org/licenses/MIT)


## Tools for editing

https://www.math.nmsu.edu/~mleisher/Software/gbdfed/

## Tools for converting

https://github.com/koron/bdf2ttf


## How to convert from source byte array to BDF file

### required tools

* gbdfed
* python 2.7+
* bdf2ttf

### convert process

1. run convert2bdf.py
2. open Micro_Font_5x5.bdf in gbdfed
3. just save file again (applies some optimization)
4. run ```bdf2ttf Micro_Font_5x5.ttf Micro_Font_5x5.ttf.ini Micro_Font_5x5.bdf```
