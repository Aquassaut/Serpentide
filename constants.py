ASIZE = 640  # size of the main window
GSIZE = 625  # size of the canvas
GFILL = "dark grey"  # color of the grid
CBG = "white"  # background color of the canvas
NBCELL = 25  # number of cells in the grid
SFILL = "black"  # segment color
OFILL = "red"  # overlapping segment color
LFILL = "blue"  # last segment color
SSIZE = GSIZE/NBCELL  # size of a segment
MIDDLE = NBCELL/2 * NBCELL  # approximate middle angle
CR = 8  # radius of helper circles
FOPT = {
    'filetypes': [
        ("Serpentide Walk file", "*.spw"),
        ("All file types", "*.*")],
    'defaultextension': '.spw'
}  # default file browser options
HCOPT = {
    'fill': "",
    'outline': "",
    'stipple': "gray25"
}  # hidden circles' options
SCOPT = {
    'fill': "brown",
    'outline': "brown",
    'stipple': "gray25"
}  # shown circles' options
