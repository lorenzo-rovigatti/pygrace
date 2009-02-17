import random

from base import BaseSet
from Styles.ColorBrewer import colorbrewer

class Color(object):
    """Object that stores a mapping between an index an a name for a color,
    as well as the RGB tuple of the color."""
    def __init__(self, index, red, green, blue, name=''):
        self.index = index
        self.red = red
        self.green = green
        self.blue = blue
        self.name = name or ('color%i' % index)

    def __str__(self):
        return '@map color %i to (%i, %i, %i), "%s"' % \
            (self.index, self.red, self.green, self.blue, self.name)

    def rgb(self):
        """Return RGB tuple."""
        return self.red, self.green, self.blue

class ColorScheme(BaseSet):
    """This subclass of the base set has a method that checks for conflicts
    in the color scheme."""
    def add_color(self, red, green, blue, name=None):
        try:
            color = self.get_item_by_name(name)
        except KeyError:
            return BaseSet.add_item(self, Color, red, green, blue, name)
        else:
            if not color.rgb() == (red, green, blue):
                message = "name '%s' cannot refer to two colors\n" % name
                message += ' ' * 12 + "old (%i, %i, %i)" % color.rgb()
                message += " != new (%i, %i, %i)" % (red, green, blue)
                raise ValueError(message)

class ColorBrewerScheme(ColorScheme):
    """Instantiate with a name of the color brewer scheme (and an optional
    number of colors -- default is the maximum that is explicitly enumerated
    in the colorbrewer definition.  The first two colors (0 and 1) are always
    white and black."""
    def __init__(self, name, n=None,reverse=False):

        # get the colors from a color brewer scheme
        try:
            scheme = colorbrewer.schemes[name]
        except KeyError:
            message = "'%s' is not a valid colorbrewer scheme name" % name
            raise KeyError(message)
        else:
            nColors = n or scheme.max_number()
            rgbList = scheme.get_colors(nColors)

        # reverse the rgb list?
        if reverse:
            rgbList = list(rgbList)
            rgbList.reverse()
            rgbList = tuple(rgbList)

        # make color instance from the rgb values
        colors = [Color(0, 255, 255, 255, 'white'), Color(1, 0, 0, 0, 'black')]
        colors.extend([Color(index + 2, r, g, b, '%s-%i' % (name, index)) \
                           for index, (r, g, b) in enumerate(rgbList)])

        ColorScheme.__init__(self, colors)

class RandomColorScheme(ColorScheme):
    """Instantiate with random seed and the number of colors.  The first
    two colors (0 and 1) are always white and black.
    """
    def __init__(self, seed,n,reverse=False):

        # create a list of rgb values
        rgbList = []
        random.seed(seed)
        for i in range(n):
            rgbList.append((random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255)))
        rgbList = tuple(rgbList)

        # reverse the rgb list?
        if reverse:
            rgbList = list(rgbList)
            rgbList.reverse()
            rgbList = tuple(rgbList)

        # make color instance from the rgb values
        name = "Rand-%d"%seed
        colors = [Color(0, 255, 255, 255, 'white'), Color(1, 0, 0, 0, 'black')]
        colors.extend([Color(index + 2, r, g, b, '%s-%i' % (name, index)) \
                           for index, (r, g, b) in enumerate(rgbList)])

        ColorScheme.__init__(self, colors)

# these are the default colors in XMGrace
default = ColorScheme([Color(*params) for params in (
        (0, 255, 255, 255, 'white'),
        (1, 0, 0, 0, 'black'),
        (2, 255, 0, 0, 'red'),
        (3, 0, 255, 0, 'green'),
        (4, 0, 0, 255, 'blue'),
        (5, 255, 255, 0, 'yellow'),
        (6, 188, 143, 143, 'brown'),
        (7, 220, 220, 220, 'grey'),
        (8, 148, 0, 211, 'violet'),
        (9, 0, 255, 255, 'cyan'),
        (10, 255, 0, 255, 'magenta'),
        (11, 255, 165, 0, 'orange'),
        (12, 114, 33, 188, 'indigo'),
        (13, 103, 7, 72, 'maroon'),
        (14, 64, 224, 208, 'turquoise'),
        (15, 0, 139, 0, 'green4'),
        )])

