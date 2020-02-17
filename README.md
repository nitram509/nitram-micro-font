
# Nitram Micro Mono

A custom pixel/bitmap based font which only needs 5x5 pixel per character.
I've used it in some older projects, back in the MS-DOS days ...
Remember when your screen resolution was only 320x200 pixel in total ;-)

![Sample: The quick brown fox jumps over the lazy dog](/the_quick_brown_fox_jumps_over_the_lazy_dog.png?raw=true)

It's source is in [CP437](https://en.wikipedia.org/wiki/Code_page_437)
code page and suitable for drawing [ASCII art](https://en.wikipedia.org/wiki/ASCII_art) ;-)

![Sample: all characters](/sample.png?raw=true)

### Difference to the CP 437 standard

Non-standard characters are highlighted in red.

![Sample: all characters](/standard_difference.png?raw=true)

## License

[MIT](https://opensource.org/licenses/MIT)


## Available formats

This font comes in various formats.

* ```nitram_micro_mono.dat``` is the historical source of this font, which I've created using some self coded tools (using Turbo Pascal)
   * pretty mutch matches the [CP437](https://en.wikipedia.org/wiki/Code_page_437) code page, and extends some custom symbols
* ```nitram-micro-mono-unicode.bdf``` is a Adobe Glyph Bitmap Distribution Format (BDF) file, generated from the source
   * use this, if you want to edit or convert into a format, suitable for existing applications (e.g. terminal font, etc.)
   * character name and character encoding refer to Unicode code points
   * preserves all known characters from [CP437](https://en.wikipedia.org/wiki/Code_page_437)
* ```nitram-micro-mono-cp1252.bdf``` is a Adobe Glyph Bitmap Distribution Format (BDF) file, generated from the source
   * use this, if you want to edit or convert into a format, suitable for existing applications (e.g. terminal font, etc.)
   * character name and character encoding refer to [CP1252](https://en.wikipedia.org/wiki/Windows-1252) code points
   * preserves just two handful extra characters from [CP437](https://en.wikipedia.org/wiki/Code_page_437), e.g. German umlauts 
* ```sources``` folder contains source files in various programming languages, which contain a bit array representation of the font
   * use these, if you want to use this font in your coding projects
      * C# [nitram_micro_mono.cs](/sources/nitram_micro_mono.cs)
      * Java [nitram_micro_mono.java](/sources/nitram_micro_mono.java)
      * Javascript [nitram_micro_mono.js](/sources/nitram_micro_mono.js)
      * Python [nitram_micro_mono.py](/sources/nitram_micro_mono.py)
   * these files where generated from the .DAT source file
      * JSON [nitram_micro_mono.json](/sources/nitram_micro_mono.json)
      * Raw data [nitram_micro_mono.dat](/nitram_micro_mono.dat)

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

Great tool for editing the font.
It heavily relies on BDF field ```ENCODING```, which refers to a Adobe's standard encoding.
According to BDF spec's this could be "-1", if no match to Adobe's standard encoding exists.
But, some converter tools don't accept this "-1" placeholder.


## How to convert font files

### BDF itself

Using gbdfed and python 2.7+

1. ```python convert2bdf.py```
2. ```gbdfed nitram-micro-mono-cp1252.bdf``` -- just open and save again ... applies some optimizations
3. ```gbdfed nitram-micro-mono-unicode.bdf``` -- just open and save again ... applies some optimizations

### BDF => TTF

Using https://github.com/koron/bdf2ttf.git

**This is a known issue.**
I've tried a couple of times to use it, but without success yet.
At least it doesnt crash, but the convered .TTF file is not showing anything.

1. ```bdf2ttf nitram-micro-mono-cp1252.ttf nitram-micro-mono.ttf.ini nitram-micro-mono-cp1252.bdf```


### BDF => FNT/FON

Using https://github.com/sunaku/bdf2fon.git

***Status*** untested

1. ```bdf2fnt nitram-micro-mono-cp1252.bdf nitram-micro-mono-cp1252.fnt```
2. ```fnt2fon nitram-micro-mono-cp1252.fnt nitram-micro-mono-cp1252.fon```
