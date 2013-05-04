ASIZE = 625  # size of the main window
GSIZE = 625  # size of the canvas
GFILL = "dark grey"  # color of the grid
CBG = "white"  # background color of the canvas
NBCELL = 25  # number of cells in the grid
SFILL = "red"  # segment color
SSIZE = GSIZE/NBCELL  # size of a segment
MIDDLE = NBCELL/2 * NBCELL  # approximate middle angle
TOL = 4  # fat finger tolerance
FOPT = {
    'filetypes': [
        ("Serpentide Walk file", "*.spw"),
        ("All file types", "*.*")],
    'defaultextension': '.spw'
}  # default file browser options
