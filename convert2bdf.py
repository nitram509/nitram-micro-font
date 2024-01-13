#!/usr/bin/python
# -*- coding: utf-8 -*-
from sources.nitram_micro_mono import nitram_micro_mono_CP437

# DANGER: please keep track, on what the single source of truth is, before enabling this!
UPDATE_DAT_FILE_FROM_PYTHON = False


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
            ('%.2x' % self.reverse_bit_order(self.bitmap_array[0])).upper(),
            ('%.2x' % self.reverse_bit_order(self.bitmap_array[1])).upper(),
            ('%.2x' % self.reverse_bit_order(self.bitmap_array[2])).upper(),
            ('%.2x' % self.reverse_bit_order(self.bitmap_array[3])).upper(),
            ('%.2x' % self.reverse_bit_order(self.bitmap_array[4])).upper(),
            'ENDCHAR'
        ]

    @staticmethod
    def reverse_bit_order(byte):
        result = 0
        for i in range(8):
            if (byte >> i) & 1:
                result |= 1 << (8 - 1 - i)
        return result


class BdfWriter:
    __BDF_ENCODING = 'ASCII'
    __BDF_NEW_LINE_SEPARATOR = '\r\n'
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
        self.bdf_file = open(file_name, "w")

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


def create_unicode_char(idx):
    unicode_char = bytearray([idx]).decode(encoding='CP437', errors='strict')[0]
    uni_code_point = ord(unicode_char)
    print("[DEBUG] idx=%.2x --> (uni)codepoint=%.4x" % (idx, uni_code_point))
    return BdfCharacter(uni_code_point, nitram_micro_mono_CP437[5 * idx:5 * idx + 5])


def create_cp1252_char(idx):
    unicode_char = bytearray([idx]).decode(encoding='CP437', errors='strict')[0]
    cp1252_char = unicode_char.encode(encoding='CP1252', errors='strict')
    cp1252_code_point = ord(cp1252_char)
    print("[DEBUG] idx=%.2x --> CP1252 codepoint=%.2x" % (idx, cp1252_code_point))
    return BdfCharacter(cp1252_code_point, nitram_micro_mono_CP437[5 * idx:5 * idx + 5])


def is_char_defined(idx):
    black_list = [
        0x00,  # empty
        0x04,  # empty
        0x08,  # empty
        0x0A,  # empty
        0x0C,  # wrong bitmap
        0x0D,  # wrong bitmap
        0x17,  # empty
        0x1D,  # wrong bitmap
        0x80,  # empty
        0x82,  # empty
        0x83,  # empty
        0x85,  # empty
        0x86,  # empty
        0x87,  # wrong bitmap
        0x88,  # wrong bitmap
        0x89,  # wrong bitmap
        0x8A,  # empty
        0x8B,  # wrong bitmap
        0x8C,  # wrong bitmap
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
        0x9B,  # wrong bitmap
        0x9D,  # wrong bitmap
        0x9E,  # empty
        0x9F,  # wrong bitmap
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
        0xE3,  # wrong bitmap
        0xE4,  # wrong bitmap
        0xE5,  # wrong bitmap
        0xE6,  # empty
        0xE7,  # wrong bitmap
        0xE8,  # wrong bitmap
        0xE9,  # empty
        0xEC,  # wrong bitmap
        0xED,  # wrong bitmap
        0xF8,  # wrong bitmap
        0xFC,  # empty
        0xFD,  # empty
        0xFE,  # empty
        0xFF,  # empty
    ]
    return idx not in black_list


def is_char_available_in_cp1252(idx):
    unicode_char = bytearray([idx]).decode(encoding='CP437', errors='strict')[0]
    cp1252_char = unicode_char.encode(encoding='CP1252', errors='ignore')
    return len(cp1252_char)


def create_unicode_BDF_file():
    print("[INFO] create nitram-micro-mono-unicode.bdf ...")
    bdf_writer = BdfWriter('nitram-micro-mono-unicode.bdf')
    bdf_writer.write_header()
    for i in range(int(len(nitram_micro_mono_CP437) / 5)):
        if is_char_defined(i):
            bdf_writer.add_char(create_unicode_char(i))
    bdf_writer.write_chars()
    bdf_writer.close()


def create_CP1252_BDF_file():
    print("[INFO] create nitram-micro-mono-cp1252.bdf ...")
    bdf_writer = BdfWriter('nitram-micro-mono-cp1252.bdf')
    bdf_writer.write_header()
    for i in range(int(len(nitram_micro_mono_CP437) / 5)):
        if is_char_defined(i) and is_char_available_in_cp1252(i):
            bdf_writer.add_char(create_cp1252_char(i))
    bdf_writer.write_chars()
    bdf_writer.close()


def update_DAT_file():
    print("[INFO] create nitram_micro_mono.dat ...")
    all_bytes = []
    for b in nitram_micro_mono_CP437:
        all_bytes.append(b)
    with open('nitram_micro_mono.dat', 'wb') as f:
        f.write(bytearray(all_bytes))


if __name__ == '__main__':
    create_unicode_BDF_file()
    create_CP1252_BDF_file()
    if UPDATE_DAT_FILE_FROM_PYTHON:
        update_DAT_file()
