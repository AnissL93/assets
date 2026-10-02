"""Make a monospace version of Fuzzy Bubbles: fixed advance, glyphs centered, wide ones squeezed."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

W, PAD = 600, 40  # advance width; minimum side bearing total for squeezed glyphs

def build(src, dst, style):
    f = TTFont(src)
    gs, glyf, hmtx = f.getGlyphSet(), f['glyf'], f['hmtx']
    for name in f.getGlyphOrder():
        rec = DecomposingRecordingPen(gs); gs[name].draw(rec)
        g = glyf[name]
        if not rec.value:                       # empty glyph (space etc.)
            hmtx[name] = (W, 0); continue
        g.recalcBounds(glyf)
        bw = g.xMax - g.xMin
        s = min(1.0, (W - PAD) / bw) if bw else 1.0   # ponytail: plain x-squeeze, thins vertical strokes on m/w
        dx = (W - bw * s) / 2 - g.xMin * s
        pen = TTGlyphPen(None)
        rec.replay(TransformPen(pen, (s, 0, 0, 1, dx, 0)))
        glyf[name] = pen.glyph()
        glyf[name].recalcBounds(glyf)
        hmtx[name] = (W, glyf[name].xMin)
    for t in ('GPOS', 'kern', 'hdmx', 'LTSH'):   # kerning would break the grid
        if t in f: del f[t]
    f['hhea'].advanceWidthMax = W
    f['post'].isFixedPitch = 1
    f['OS/2'].xAvgCharWidth = W
    f['OS/2'].panose.bProportion = 9           # monospaced
    fam, full = 'Fuzzy Bubbles Mono', f'Fuzzy Bubbles Mono {style}'
    ps = f'FuzzyBubblesMono-{style}'
    n = f['name']
    for rec_ in list(n.names):
        if rec_.nameID in (3, 16, 17, 21, 22): n.removeNames(nameID=rec_.nameID)
    for nid, val in ((1, fam), (2, style), (3, ps), (4, full), (6, ps)):
        n.setName(val, nid, 3, 1, 0x409); n.setName(val, nid, 1, 0, 0)
    f.save(dst)

if __name__ == '__main__':
    build(*sys.argv[1:4])
