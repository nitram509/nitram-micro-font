#!/usr/bin/python
# -*- coding: utf-8 -*-

from sources.nitram_micro_mono import nitram_micro_mono_CP437

class BdfCharacter:
    def __init__(self, code_point, bitmap_array):
        self.code_point = code_point
        self.bitmap_array = bitmap_array

    def as_text_lines(self):
        return [
            'STARTCHAR char%d' % self.code_point,
            'ENCODING %d' % self.code_point,
            'SWIDTH 225 0',
            'DWIDTH 5 0',
            'BBX 5 5 0 0',
            'BITMAP',
            '%.2x' % self.reverse_bit_order(self.bitmap_array[0]),
            '%.2x' % self.reverse_bit_order(self.bitmap_array[1]),
            '%.2x' % self.reverse_bit_order(self.bitmap_array[2]),
            '%.2x' % self.reverse_bit_order(self.bitmap_array[3]),
            '%.2x' % self.reverse_bit_order(self.bitmap_array[4]),
            'ENDCHAR'
        ]

    def reverse_bit_order(self, byte):
        result = 0
        for i in xrange(8):
            if (byte >> i) & 1: result |= 1 << (8 - 1 - i)
        return result


class BdfWriter:
    __BDF_ENCODING = 'ASCII'
    __BDF_NEW_LINE_SEPARATOR = str('\r\n'.encode(encoding=__BDF_ENCODING))
    __BDF_START_FONT = [
        'STARTFONT 2.2',
        'COMMENT A monospaced micro font. Uppercase chars only.',
        'FONT -Nitram-Micro-Mono',
        'SIZE 5 320 200',
        'FONTBOUNDINGBOX 5 5 0 0',
        'STARTPROPERTIES 4',
        'MinSpace "5"',
        'Copyright "Copyright (c) 1996 Martin W. Kirst"',
        'FONT_ASCENT 5',
        'FONT_DESCENT 5',
        'ENDPROPERTIES',
    ]

    def __init__(self, file_name):
        self.__chars = []
        self.data = []
        self.bdf_file = file(file_name, "w")

    def add_char(self, bdf_character):
        self.__chars.append(bdf_character)

    def write_header(self):
        for line in self.__BDF_START_FONT:
            self.bdf_file.write(line)
            self.__write_new_line()
        self.__write_bdf_number_of_chars()

    def write_chars(self):
        for character in self.__chars:
            for line in character.as_text_lines():
                self.bdf_file.write(line)
                self.__write_new_line()

    def close(self):
        self.__write_bdf_end_font()
        self.bdf_file.close()

    def __write_bdf_end_font(self):
        self.bdf_file.write('ENDFONT')
        self.__write_new_line()

    def __write_bdf_number_of_chars(self):
        self.bdf_file.write('CHARS %d' % len(self.__chars))
        self.__write_new_line()

    def __write_new_line(self):
        self.bdf_file.write(self.__BDF_NEW_LINE_SEPARATOR)


def create_char(idx):
    unicode_char = unicode(chr(idx), encoding='CP437', errors='strict')
    uni_code_point = ord(unicode_char)
    cp1252_char = unicode_char.encode(encoding='CP1252', errors='ignore')
    if len(cp1252_char) > 0:
        cp1252_code_point = ord(cp1252_char)
        print "[INFO] idx=%.2x --> (uni)codepoint=%.4x --> CP1252 codepoint=%.2x" % (idx, uni_code_point, cp1252_code_point)
    else:
        print "[INFO] idx=%.2x --> (uni)codepoint=%.4x" % (idx, uni_code_point)
    return BdfCharacter(uni_code_point, nitram_micro_mono_CP437[5 * idx:5 * idx + 5])


def is_char_defined(idx):
    black_list = [
        0x00,  # empty
        0x04,  # empty
        0x08,  # empty
        0x0A,  # empty
        0x17,  # empty
        0x80,  # empty
        0x82,  # empty
        0x83,  # empty
        0x85,  # empty
        0x86,  # empty
        0x8A,  # empty
        0x8D,  # empty
        0x8F,  # empty
        0x90,  # empty
        0x91,  # empty
        0x92,  # empty
        0x93,  # empty
        0x95,  # empty
        0x96,  # wrong bitmap
        0x97,  # wrong bitmap
        0x98,  # wrong bitmap
        0x9C,  # empty
        0x9E,  # empty
        0xA0,  # empty
        0xA1,  # empty
        0xA2,  # empty
        0xA3,  # empty
        0xA4,  # empty
        0xA5,  # empty
        0xA6,  # empty
        0xA7,  # empty
        0xAB,  # empty
        0xAC,  # empty
        0xE0,  # empty
        0xE2,  # empty
        0xE6,  # empty
        0xE9,  # empty
        0xEA,  # empty
        0xEB,  # empty
        0xFC,  # empty
        0xFD,  # empty
        0xFE,  # empty
        0xFF,  # empty
        0x0C,  # wrong bitmap
        0x0D,  # wrong bitmap
        0x1D,  # wrong bitmap
        0x87,  # wrong bitmap
        0x88,  # wrong bitmap
        0x89,  # wrong bitmap
        0x8B,  # wrong bitmap
        0x8C,  # wrong bitmap
        0x9B,  # wrong bitmap
        0x9D,  # wrong bitmap
        0x9F,  # wrong bitmap
        0xE3,  # wrong bitmap
        0xE4,  # wrong bitmap
        0xE5,  # wrong bitmap
        0xE7,  # wrong bitmap
        0xE8,  # wrong bitmap
        0xEC,  # wrong bitmap
        0xF8,  # wrong bitmap

    ]
    return idx not in black_list


if __name__ == '__main__':
    bdf_writer = BdfWriter('nitram-micro-mono.bdf')
    bdf_writer.write_header()
    for i in xrange(len(nitram_micro_mono_CP437) / 5):
        if is_char_defined(i):
            bdf_writer.add_char(create_char(i))
    bdf_writer.write_chars()
    bdf_writer.close()
