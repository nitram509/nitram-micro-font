
# Nitram Micro Mono

A custom pixel/bitmap based font which only needs 5x5 pixel per character.
I've used it in some older projects, back in the MS-DOS days ...
Remember when your screen resolution was only 320x200 pixel in total ;-)

![Sample: The quick brown fox jumps over the lazy dog](/the_quick_brown_fox_jumps_over_the_lazy_dog.png?raw=true)

It's source is in [CP437](https://en.wikipedia.org/wiki/Code_page_437)
code page and suitable for drawing [ASCII art](https://en.wikipedia.org/wiki/ASCII_art) ;-)

![Sample: all characters](/sample.png?raw=true)

## License

[MIT](https://opensource.org/licenses/MIT)


## Available formats

This font comes in various formats.

* ```nitram_micro_mono.dat``` is the historical source of this font, which I've created using some self coded tools (using Turbo Pascal)
   * pretty mutch matches the CP4437 code page, and extends some custom symbols
* ```nitram-micro-mono-unicode.bdf``` is a Adobe Glyph Bitmap Distribution Format (BDF) file, generated from the source
   * use this, if you want to edit or convert into a format, suitable for existing applications (e.g. terminal font, etc.)
   * character name and character encoding refer to Unicode code points
   * preserves all known characters from CP437
* ```nitram-micro-mono-cp1252.bdf``` is a Adobe Glyph Bitmap Distribution Format (BDF) file, generated from the source
   * use this, if you want to edit or convert into a format, suitable for existing applications (e.g. terminal font, etc.)
   * character name and character encoding refer to CP1252 code points
   * preserves just two handful extra characters from CP437, e.g. German umlauts 
* ```sources``` folder contains source files in various programming languages, which contain a bit array representation of the font
   * use these, if you want to use this font in your coding projects
   * these files where generated from the .DAT source file

## How to render

This is a naive Javascript implementation, rendering pixel by pixel on a HTML5 canvas.

```javascript
function drawMicroFont_100percent_putPixel_like(canvas) {
  var context = canvas.getContext("2d");
  for (var c = 0; c < nitram_micro_mono_CP437.length / 5; c++) {
    var charImageData = context.createImageData(5, 5);
    var img = charImageData.data;
    for (var y = 0; y < 5; y++) {
      for (var x = 0; x < 5; x++) {
        if ((nitram_micro_mono_CP437[c * 5 + y] & (1 << x)) == (1 << x)) {
          var offs = y * 5 + x;
          img[offs * 4]     = 0;
          img[offs * 4 + 1] = 0;
          img[offs * 4 + 2] = 0;
          img[offs * 4 + 3] = 255;
        }
      }
    }
    context.putImageData(charImageData, (c % 16) * 6, 6 * Math.floor(c / 16));
  }
}
```

## Tools for editing

https://www.math.nmsu.edu/~mleisher/Software/gbdfed/

***Status***
Great tool for editing the font.
It heavily relies on BDF field ```ENCODING```, which refers to a Adobe's standard encoding.
According to BDF spec's this could be "-1", if no match to Adobe's standard encoding exists.
But, some converter tools don't accept this "-1" placeholder.

## Tools for converting

https://github.com/koron/bdf2ttf

***Status*** 
**This is a known issue.**
I've tried a couple of times to use it, but without success yet.
At least it doesnt crash, but the convered .TTF file is not showing anything.


## How to convert from source byte array to BDF file

### required tools

* gbdfed
* python 2.7+
* bdf2ttf

### convert process

1. run convert2bdf.py
2. open Micro_Font_5x5.bdf in gbdfed
3. just save file again (applies some optimization)
4. run ```bdf2ttf Micro_Font_5x5.ttf Micro_Font_5x5.ttf.ini Micro_Font_5x5.bdf```       <<== NOT working yet!

#### BDF => FNT/FON

Using https://github.com/sunaku/bdf2fon.git

***Status*** untested

1. bdf2fnt nitram-micro-mono-cp1252.bdf nitram-micro-mono-cp1252.fnt 
2. fnt2fon nitram-micro-mono-cp1252.fnt nitram-micro-mono-cp1252.fon