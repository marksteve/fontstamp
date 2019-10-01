from base64 import b64encode
from io import BytesIO
from xml.sax.saxutils import unescape

import xmltodict
from fontTools.subset import Options, Subsetter, load_font, save_font

# https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids
NAME_ID_FONT_NAME = 4


def font_name(font):
    return font["name"].names[NAME_ID_FONT_NAME].toStr()


def subset_font(font, text, options):
    subsetter = Subsetter(options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    with BytesIO() as outfile:
        save_font(font, outfile, options)
        outfile.seek(0)
        out = b64encode(outfile.read())
    return out.decode()


def stamp(svgfile, fontfile, text, font_family=None, xml_transform=None):
    options = Options(flavor="woff2")
    with load_font(fontfile, options) as font:
        font_family = font_family or font_name(font)
        font_data = subset_font(font, text, options)
    with open(svgfile) as f:
        xml = xmltodict.parse(f.read())
    # Embed font in root style tag
    style = xml["svg"].get("style", {"#text": ""})
    if type(style) == str:
        style = {"#text": style}
    style[
        "#text"
    ] += f"""
<![CDATA[
@font-face {{
  font-family: "{font_family}";
  src: url("data:font/woff2;base64,{font_data}");
}}
]]>
"""
    xml["svg"]["style"] = style
    if xml_transform:
        xml = xml_transform(xml)
    return unescape(xmltodict.unparse(xml))
