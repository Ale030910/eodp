# TEST LEVEL-1C
#
# 1. Plot L1B grid (red) vs L1C grid (blue)
# 2. SSD of the central row of the L1B geometry
# 3. SSD of the central column of the L1B geometry


import os
import numpy as np
import matplotlib.pyplot as plt

from netCDF4 import Dataset
from geopy.distance import distance

from common.io.readGeodetic import readGeodetic


# =========================================================================
# DIRECTORIES
# =========================================================================

# L1B geometry
gmdir = (
    r'C:\Users\aleja\Desktop\SHARED\EODP_TER_2021'
    r'\EODP-TS-L1C\input\gm_alt100_act_150'
)

# L1C outputs
l1cdir = (
    r'C:\Users\aleja\Desktop\SHARED\EODP_TER_2021'
    r'\EODP-TS-L1C\myoutputs'
)

geolocation_file = 'geolocation.nc'

l1c_file = os.path.join(
    l1cdir,
    'l1c_toa_VNIR-0.nc'
)


# =========================================================================
# READ L1C GEOLOCATION
# =========================================================================

def readL1cGeolocation(filename):

    nc = Dataset(filename, 'r')

    lat = np.array(nc.variables['lat'][:]).squeeze()
    lon = np.array(nc.variables['lon'][:]).squeeze()

    nc.close()

    return lat, lon


# =========================================================================
# TEST 1
# L1B GRID VS L1C GRID
# =========================================================================

def plotGrids(lat_l1b, lon_l1b, lat_l1c, lon_l1c):

    plt.figure(figsize=(10, 7))

    # L1B grid - RED
    plt.scatter(
        lon_l1b.flatten(),
        lat_l1b.flatten(),
        s=2,
        c='red',
        label='L1B grid'
    )

    # L1C grid - BLUE
    plt.scatter(
        lon_l1c.flatten(),
        lat_l1c.flatten(),
        s=5,
        c='blue',
        label='L1C grid'
    )

    plt.xlabel('Longitude [deg]')
    plt.ylabel('Latitude [deg]')
    plt.title('L1B grid vs L1C grid')

    plt.legend()
    plt.grid()

    plt.savefig(
        os.path.join(
            l1cdir,
            'test_L1B_vs_L1C_grid.png'
        ),
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()


# =========================================================================
# TEST 2
# SSD - CENTRAL ROW
# =========================================================================

def calculateSSDcentralRow(lat, lon):
    """
    Calculate the spatial sampling distance along the
    central row of the L1B geometry.

    The image has 150 ACT pixels, therefore there are
    149 distances between consecutive pixels.
    """

    central_row = lat.shape[0] // 2

    ssd = []

    for j in range(lat.shape[1] - 1):

        point1 = (
            lat[central_row, j],
            lon[central_row, j]
        )

        point2 = (
            lat[central_row, j + 1],
            lon[central_row, j + 1]
        )

        d = distance(
            point1,
            point2
        ).meters

        ssd.append(d)

    return np.array(ssd)


def plotSSDcentralRow(ssd):

    # 149 intervals between 150 ACT pixels
    pixels = np.arange(1, len(ssd) + 1)

    plt.figure(figsize=(10, 6))

    plt.plot(
        pixels,
        ssd
    )

    plt.xlabel('ACT pixel')
    plt.ylabel('SSD [m]')
    plt.title('SSD - Central row of L1B geometry')

    # Show the complete detector width
    plt.xlim(0, 150)

    plt.grid()

    plt.savefig(
        os.path.join(
            l1cdir,
            'test_SSD_central_row.png'
        ),
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()


# =========================================================================
# TEST 3
# SSD - CENTRAL COLUMN
# =========================================================================

def calculateSSDcentralColumn(lat, lon):
    """
    Calculate the spatial sampling distance along the
    central column of the L1B geometry.

    The image has 100 ALT lines, therefore there are
    99 distances between consecutive pixels.
    """

    central_column = lat.shape[1] // 2

    ssd = []

    for i in range(lat.shape[0] - 1):

        point1 = (
            lat[i, central_column],
            lon[i, central_column]
        )

        point2 = (
            lat[i + 1, central_column],
            lon[i + 1, central_column]
        )

        d = distance(
            point1,
            point2
        ).meters

        ssd.append(d)

    return np.array(ssd)


def plotSSDcentralColumn(ssd):

    # 99 intervals between 100 ALT pixels
    pixels = np.arange(1, len(ssd) + 1)

    plt.figure(figsize=(10, 6))

    plt.plot(
        pixels,
        ssd
    )

    plt.xlabel('ALT pixel')
    plt.ylabel('SSD [m]')
    plt.title('SSD - Central column of L1B geometry')

    plt.xlim(0, 100)

    plt.grid()

    plt.savefig(
        os.path.join(
            l1cdir,
            'test_SSD_central_column.png'
        ),
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()


# =========================================================================
# MAIN
# =========================================================================

if __name__ == '__main__':

    # ---------------------------------------------------------------------
    # READ L1B GEOLOCATION
    # ---------------------------------------------------------------------

    print('Reading L1B geolocation...')

    lat_l1b, lon_l1b = readGeodetic(
        gmdir,
        geolocation_file
    )

    print('L1B grid shape:', lat_l1b.shape)

    print(
        'Central row:',
        lat_l1b.shape[0] // 2
    )

    print(
        'Central column:',
        lat_l1b.shape[1] // 2
    )


    # ---------------------------------------------------------------------
    # READ L1C GEOLOCATION
    # ---------------------------------------------------------------------

    print('\nReading L1C geolocation...')

    lat_l1c, lon_l1c = readL1cGeolocation(
        l1c_file
    )

    print(
        'Number of L1C points:',
        len(lat_l1c)
    )


    # =====================================================================
    # TEST 1
    # L1B GRID RED VS L1C GRID BLUE
    # =====================================================================

    plotGrids(
        lat_l1b,
        lon_l1b,
        lat_l1c,
        lon_l1c
    )


    # =====================================================================
    # TEST 2
    # SSD CENTRAL ROW
    # =====================================================================

    ssd_row = calculateSSDcentralRow(
        lat_l1b,
        lon_l1b
    )

    print('\n-------------------------------')
    print('SSD CENTRAL ROW')
    print('-------------------------------')
    print('Mean =', np.mean(ssd_row), 'm')
    print('Min  =', np.min(ssd_row), 'm')
    print('Max  =', np.max(ssd_row), 'm')

    plotSSDcentralRow(
        ssd_row
    )


    # =====================================================================
    # TEST 3
    # SSD CENTRAL COLUMN
    # =====================================================================

    ssd_column = calculateSSDcentralColumn(
        lat_l1b,
        lon_l1b
    )

    print('\n-------------------------------')
    print('SSD CENTRAL COLUMN')
    print('-------------------------------')
    print('Mean =', np.mean(ssd_column), 'm')
    print('Min  =', np.min(ssd_column), 'm')
    print('Max  =', np.max(ssd_column), 'm')

    plotSSDcentralColumn(
        ssd_column
    )