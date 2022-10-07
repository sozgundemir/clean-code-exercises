# TODO: refactor & clean up this class.
#  - Familiarize yourself with the code and what it does (it is easiest to read the tests first)
#  - refactor ...
#     - give the functions/variables proper names
#     - make the function bodies more readable
#     - clean up the test code where beneficial
#     - make sure to put each individual change in a small, separate commit
#     - take care that on each commit, all tests pass
from typing import Tuple
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

class RasterGrid:
    @dataclass
    class Cell:
        _ix: int
        _iy: int

    def __init__(self,
                 lowerLeft: Point,
                 size: Tuple[float, float],
                 nx: int,
                 ny: int) -> None:
        self._lowerLeft = lowerLeft
        self._upperRight = Point(
            self._lowerLeft.x+size[0],
            self._lowerLeft.y+size[1])
        self._nx = nx
        self._ny = ny
        self._nc = nx*ny
        self.cells = [
            self.Cell(i, j) for i in range(nx) for j in range(ny)
        ]

    @property
    def nc(self) -> int:
        return self._nc

    def getCellCenter(self, cell: Cell) -> Point:
        centerX = self._lowerLeft.x + (float(cell._ix) + 0.5) * (self._upperRight.x - self._lowerLeft.x) / self._nx
        centerY = self._lowerLeft.y + (float(cell._iy) + 0.5) * (self._upperRight.y - self._lowerLeft.y) / self._ny
        return Point(centerX, centerY)

    def getContainingCell(self, x: float, y: float) -> Cell:
        # returns the cell in the rastergrid containing the given position
        # Calculate the max step distance in x-, y- directions
        eps = 1e-6*max(
            (self._upperRight.x-self._lowerLeft.x)/self._nx,
            (self._upperRight.y-self._lowerLeft.y)/self._ny
        )
        # return extreme index values if given x position is close to one of the
        # boundaries less than eps
        if abs(x - self._upperRight.x) < eps:
            ix = self._nx - 1
        elif abs(x - self._lowerLeft.x) < eps:
            ix = 0
        else:
            ix = int((x - self._lowerLeft.x)/((self._upperRight.x - self._lowerLeft.x)/self._nx))
        # return extreme index values if given y position is close to one of the
        # boundaries less than eps
        if abs(y - self._upperRight.y) < eps:
            iy = self._ny - 1
        elif abs(y - self._lowerLeft.y) < eps:
            iy = 0
        else:
            iy = int((y - self._lowerLeft.y)/((self._upperRight.y - self._lowerLeft.y)/self._ny))
        return self.Cell(ix, iy)

def test_number_of_cells():
    # This function tests if the the grid can be created with the correct number
    # of cells
    x0 = 0.0
    y0 = 0.0
    dx = 1.0
    dy = 1.0
    assert RasterGrid(Point(x0, y0), (dx, dy), 10, 10).nc == 100
    assert RasterGrid(Point(x0, y0), (dx, dy), 10, 20).nc == 200
    assert RasterGrid(Point(x0, y0), (dx, dy), 20, 10).nc == 200
    assert RasterGrid(Point(x0, y0), (dx, dy), 20, 20).nc == 400

def test_locate_cell():
    # This function tests if the containing cell of a given position can be
    # received correctly
    grid = RasterGrid(Point(0.0, 0.0), (2.0, 2.0), 2, 2)
    cell = grid.getContainingCell(0, 0)
    assert cell._ix == 0 and cell._iy == 0
    cell = grid.getContainingCell(1, 1)
    assert cell._ix == 1 and cell._iy == 1
    cell = grid.getContainingCell(0.5, 0.5)
    assert cell._ix == 0 and cell._iy == 0
    cell = grid.getContainingCell(1.5, 0.5)
    assert cell._ix == 1 and cell._iy == 0
    cell = grid.getContainingCell(0.5, 1.5)
    assert cell._ix == 0 and cell._iy == 1
    cell = grid.getContainingCell(1.5, 1.5)
    assert cell._ix == 1 and cell._iy == 1


def test_cell_center():
    grid = RasterGrid(Point(0.0, 0.0), (2.0, 2.0), 2, 2)
    cell = grid.getContainingCell(0.5, 0.5)
    assert abs(grid.getCellCenter(cell).x - 0.5) < 1e-7 and abs(grid.getCellCenter(cell).y - 0.5) < 1e-7
    cell = grid.getContainingCell(1.5, 0.5)
    assert abs(grid.getCellCenter(cell).x - 1.5) < 1e-7 and abs(grid.getCellCenter(cell).y - 0.5) < 1e-7
    cell = grid.getContainingCell(0.5, 1.5)
    assert abs(grid.getCellCenter(cell).x - 0.5) < 1e-7 and abs(grid.getCellCenter(cell).y - 1.5) < 1e-7
    cell = grid.getContainingCell(1.5, 1.5)
    assert abs(grid.getCellCenter(cell).x - 1.5) < 1e-7 and abs(grid.getCellCenter(cell).y - 1.5) < 1e-7


def test_cell_iterator() -> None:
    grid = RasterGrid(Point(0.0, 0.0), (2.0, 2.0), 2, 2)
    count = sum(1 for _ in grid.cells)
    assert count == grid.nc

    cell_indices_without_duplicates = set(list(
        (cell._ix, cell._iy) for cell in grid.cells
    ))
    assert len(cell_indices_without_duplicates) == count

test_number_of_cells()
test_locate_cell()
test_cell_center()
test_cell_iterator()