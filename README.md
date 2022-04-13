# detector_geometry
#### A tool to project resolution cones at different detector geometries (tilt, rotation, offset) and X-ray energies
 - Main application is to visualize the maximum achievable resolution at a given geometry
 - The math used is not meant to bring people to the moon but to provide a quick and simple preview
 - The module building code is designed for [Dectris](https://www.dectris.com) [Pilatus3](https://www.dectris.com/detectors/x-ray-detectors/pilatus3/) and [Eiger2](https://www.dectris.com/detectors/x-ray-detectors/eiger2/) Detectors but one-module systems like the [Bruker](https://www.bruker.com/en.html) [Photon II](https://www.bruker.com/en/products-and-solutions/diffractometers-and-scattering-systems/single-crystal-x-ray-diffractometers/sc-xrd-components/detectors.html) are possible as well
 - It uses [python3](https://www.python.org), [numpy](https://numpy.org) and [matplotlib 3.5.1](https://matplotlib.org)

## Short how-to:
 - Edit the .py file:
   - Choose a detector (Eiger2 or Pilatus3)
   - Choose a model (300K, 1M, 2M, etc.)
 - run it
 - Use the sliders to change energy and geometry
 - Use the radio buttons to change contour units

## Here's an example showing a rotated Eiger2 4M:
![Image](../main/_lib/Eiger2_CdTe_4M_interactive.png)

##### Limits and Plot details can be changed in the .py file

## To add a detector:
 - Choose 'Name' and 'Version' (will be used in the figure title)
 - 'Name' must not start with 'Pilatus' or 'Eiger', those are pre-set

 |   Geometry   |   Value   | Hint |
 |--------------|-----------|------|
 | geo.det_type | 'Name'    | [str]  Pilatus3 / Eiger2
 | geo.det_size | 'Version' | [str]  300K 1M 2M 6M / 1M 4M 9M 16M

 - Adjust the "ADD CUSTOM DETECTOR SPECIFICATIONS HERE" section
 - The pixel size is only used to calculate the gap size

 | Detector |       Value       | Hint |
 |----------|-------------------|------|
 | det.name | 'Name Version'    | [auto] Generated
 | det.hms  | 100.0             | [mm]   Module size (horizontal)
 | det.vms  | 140.0             | [mm]   Module size (vertical)
 | det.pxs  | 50e-3             | [mm]   Pixel size
 | det.hgp  | 0                 | [pix]  Gap between modules (horizontal)
 | det.vgp  | 0                 | [pix]  Gap between modules (vertical)
 | det.hmn  | 1                 | [int]  Number of modules (horizontal)
 | det.vmn  | 1                 | [int]  Number of modules (vertical)
 
##### I hope this turns out to be useful for someone!
