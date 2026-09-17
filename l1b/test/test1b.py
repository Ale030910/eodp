# CROSS VALIDATE L1B OUTPUTS EQUALIZED

# PLOT FROM YOUR OUTPUTS THE EQUALISED OUTPUT VERSUS NOT EQUALISED VERSUS THE TRUTH
# TRUTH = EODP-TS-L1B\input\ism_toa_isrf_VNIR-0.nc

# CROSS VALIDATE L1B OUTPUTS EQUALIZED

from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt


# -------------------------------------------------------------------------
# Project root
# -------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from common.io.writeToa import readToa
from common.src.auxFunc import getIndexBand
from l1b.src.l1b import l1b


# -------------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------------
base_dir = Path(
    r"C:\Users\aleja\Desktop\SHARED\EODP_TER_2021\EODP-TS-L1B"
)

aux_dir = PROJECT_ROOT / "auxiliary"

input_dir = base_dir / "input"

# Outputs de la profesora
reference_dir = base_dir / "output"

# Mis outputs
my_output_dir = base_dir / "myoutputs"


# -------------------------------------------------------------------------
# Bands
# -------------------------------------------------------------------------
bands = [
    "VNIR-0",
    "VNIR-1",
    "VNIR-2",
    "VNIR-3"
]


# =========================================================================
# 1. CROSS VALIDATION
# =========================================================================

print("\n========================================")
print("CROSS VALIDATION L1B - EQUALIZATION")
print("========================================")


for band in bands:

    print("\n----------------------------------------")
    print("BAND:", band)
    print("----------------------------------------")

    filename = "l1b_toa_eq_" + band + ".nc"

    # Output de referencia de la profesora
    toa_reference = readToa(
        str(reference_dir),
        filename
    )

    # Mi output
    toa_mine = readToa(
        str(my_output_dir),
        filename
    )

    # Diferencia
    difference = toa_mine - toa_reference

    max_error = np.max(np.abs(difference))
    mean_error = np.mean(np.abs(difference))
    rmse = np.sqrt(np.mean(difference ** 2))

    print("Maximum absolute error:", max_error)
    print("Mean absolute error:", mean_error)
    print("RMSE:", rmse)

    if np.allclose(
        toa_mine,
        toa_reference,
        rtol=1e-6,
        atol=1e-6
    ):

        print(
            "RESULT: OK - My equalized output matches the reference."
        )

    else:

        print(
            "RESULT: ERROR - My equalized output does NOT match the reference."
        )


# =========================================================================
# 2. PLOT
#
# Equalized vs Not Equalized vs Truth
# VNIR-0
# =========================================================================

band = "VNIR-0"


# -------------------------------------------------------------------------
# Create L1B object only to obtain the gain from the configuration
# -------------------------------------------------------------------------
myL1b = l1b(
    str(aux_dir).replace("\\", "/"),
    str(input_dir).replace("\\", "/"),
    str(my_output_dir).replace("\\", "/")
)

gain = myL1b.l1bConfig.gain[
    getIndexBand(band)
]

print("\nGain", band, "=", gain)


# -------------------------------------------------------------------------
# NOT EQUALIZED
#
# Input to L1B.
# It is in DN, so we only apply the absolute gain to express it
# in radiances WITHOUT applying equalization.
# -------------------------------------------------------------------------
toa_not_equalized_dn = readToa(
    str(input_dir),
    "ism_toa_" + band + ".nc"
)

toa_not_equalized = toa_not_equalized_dn * gain


# -------------------------------------------------------------------------
# EQUALIZED
#
# Final L1B output:
# equalization + restoration
# Already in radiances.
# -------------------------------------------------------------------------
toa_equalized = readToa(
    str(my_output_dir),
    "l1b_toa_" + band + ".nc"
)


# -------------------------------------------------------------------------
# TRUTH
#
# File specified in test1b.py
# -------------------------------------------------------------------------
toa_truth = readToa(
    str(input_dir),
    "ism_toa_isrf_" + band + ".nc"
)


# -------------------------------------------------------------------------
# Select one ALT line
# -------------------------------------------------------------------------
alt_line = 1


# -------------------------------------------------------------------------
# Plot
# -------------------------------------------------------------------------
plt.figure(figsize=(12, 7))


plt.plot(
    toa_not_equalized[alt_line, :],
    label="Not equalized"
)


plt.plot(
    toa_equalized[alt_line, :],
    label="Equalized"
)


plt.plot(
    toa_truth[alt_line, :],
    label="Truth"
)


plt.xlabel("ACT pixel [-]")

plt.ylabel("TOA [mW/m2/sr]")

plt.title(
    "L1B Equalization Cross-validation for " + band
)

plt.legend()

plt.grid()

plt.tight_layout()

plt.show()