from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.lib import colors

from reportlab.graphics.shapes import Rect, Circle
from reportlab.lib.colors import CMYKColorSep

green = CMYKColorSep(60, 0, 30, 0, spotName='green')

###################################################################
# To create the mirrored pdf using ghostscript
########
# sb-mbp:python-reportlab-papermaker boylesa$ gs                 \
# >   -o mirrored-horizonal.pdf                                  \
# >   -sDEVICE=pdfwrite                                          \
# >   -dAutoRotatePages=/None                                    \
# >   -c "<</Install{595 0 translate -1 1 scale}>>setpagedevice" \
# >   -f squared.pdf
###################################################################

class Squared_paper(object):
    def __init__(self):
        self.filename = "squared.pdf"
        self.papersize = "A4"
        self.heavierline = 0
        self.gridspacing = -0.5
        self.gridborder = 2
        self.color = colors.darkslateblue

    def create(self, filename="squared.pdf"):
        graphpaper(self.filename, self.papersize, self.heavierline, self.gridspacing, self.gridborder, self.color)


def graphpaper(filename, papersize, heavierline, gridspacing, gridborder, color):
    # rcolor = {"Black":black, "Gray":gray, "Red":red, "Green":green, "Blue":blue, "Yellow":yellow}
    #
    # Currently only two papersize options: Letter or A4
    #
    if (papersize == "Letter"):
        ps = letter
    else:
        ps = A4
    #
    # Negative gridspacing means cm
    #
    if (gridspacing < 0):
        unit = cm
        gs = -gridspacing
    else:
        unit = inch
        gs = gridspacing
    #
    # Create the reportlab canvas
    #
    c = canvas.Canvas(filename, pagesize=ps)
    paperwidth = ps[0] * 0.96
    paperheight = ps[1]

    # paperheight adjustment for title space
    paperheight = paperheight - 1 * cm

    spacing = gs * unit
    #
    # Adjust hgrid and vgrid to provide a border of width at least the
    # size of gridborder multiples of the grid spacing.
    #
    hgrid = int(paperwidth / spacing) - 2 * gridborder
    vgrid = int(paperheight / spacing) - 2 * gridborder
    #
    # If heavier lines will be drawn, we adjust hgrid and vgrid to
    # be multiples of heavierline.  Then the outer most grid lines
    # around the whole grid will be heavy lines.
    #
    if (heavierline > 0):
        hgrid = heavierline * (hgrid / heavierline)
        vgrid = heavierline * (vgrid / heavierline)
    #
    # These are the actual width and height of the grid (in points)
    #
    actualgraphwidth = hgrid * spacing
    actualgraphheight = vgrid * spacing
    #
    # If we are not filling the page, we move the origin so that
    # the grid is centered.
    #
    hoffset = (paperwidth - actualgraphwidth) / 2.0
    voffset = (paperheight - actualgraphheight) / 2.0
    c.translate(hoffset, voffset)
    #
    # The next two if statements check if we might end up trying to
    # draw the lines across the entire page.  If so, subtract one
    # from the lengths.
    #
    if (actualgraphheight == paperheight):
        actualgraphheight = actualgraphheight - 1

    if (actualgraphwidth == paperwidth):
        actualgraphwidth = actualgraphwidth - 1

    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    m = heavierline

    line_width = 0.15
    #
    # Draw the vertical lines
    #
    for i in range(hgrid + 1):
        if (m > 0 and i % m == 0):
            c.setLineWidth(1.0)
        else:
            c.setLineWidth(line_width)

        if (i * spacing == paperwidth):
            x = i * spacing - 1
        else:
            x = i * spacing
        c.line(x, 0, x, actualgraphheight)
    #
    # Draw the horizontal lines
    #
    for i in range(vgrid + 1):
        if (m > 0 and i % m == 0):
            c.setLineWidth(1.0)
        else:
            c.setLineWidth(line_width)
        if (i * spacing == paperheight):
            y = i * spacing - 1
        else:
            y = i * spacing
        c.line(0, y, actualgraphwidth, y)
    #
    # Call the ReportLab canvas functions to create the file.
    #

    # Draw a title block for page labelling
    #
    # c.line(x, 0, x, 1) # vertical left
    # c.line(x, 0, x, 1) # vertical right

    c.setStrokeColor(color)
    c.setLineWidth = 1

    c.line(0, actualgraphheight + (0.2 * cm), actualgraphwidth, actualgraphheight + (0.2 * cm))  # horizontal bottom
    c.line(0, actualgraphheight + (1.0 * cm), actualgraphwidth, actualgraphheight + (1.0 * cm))  # horizontal top
    c.line(0, actualgraphheight + (0.2 * cm), 0, actualgraphheight + (1.0 * cm))                 # vertical left
    c.line(actualgraphwidth, actualgraphheight + (0.2 * cm), actualgraphwidth,
           actualgraphheight + (1.0 * cm))  # vertical right

    # Draw the colour tab
    c.setFillOverprint(True)

    c.setFillColor(green)
    # c.rect(-10, 0, -50, 100, stroke=1, fill=1)
    c.rect(-20, -40, -20, 1000, stroke=1, fill=1)  # Full length
    c.circle(paperwidth - 35, (paperheight * 0.5) + 90, 5, stroke=1, fill=0)  # Punch hole
    c.circle(paperwidth - 35, (paperheight * 0.5) - 90, 5, stroke=1, fill=0)  # Punch hole
    c.circle(paperwidth - 35, (paperheight * 0.5) + 270, 5, stroke=1, fill=0)  # Punch hole
    c.circle(paperwidth - 35, (paperheight * 0.5) - 270, 5, stroke=1, fill=0)  # Punch hole

    c.showPage()
    c.save()


if __name__ == "__main__":
    paper_template = Squared_paper()
    paper_template.create()
