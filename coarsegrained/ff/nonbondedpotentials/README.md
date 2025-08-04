The HOOMD-Blue engine requires the tabulated potential information to be dimensionless


Therefore, the non-bonded parameters used in running an actual simulation are the the txt files in the folder "dimensionlesspotentials" 
column 1: distance r (unitless)
column 2: potential energy (unitless)
column 3: force (unitless)

In the "scaledpotentials" folder, are the original dimensionless potentials but scaled to have some kind of units associated with them 
column 1: distance r (nm)
column 2: potential energy (kJ/mol)
column 3: force (kJ/mol-nm)

Because in one of our manual hoomd-funcs has the unit information, in the python file units.py and the excerpt below,
def get_units():
    units = {}
    units['t'] = 7873.6037  # fs
    units['M'] = 72.056  # amu
    units['D'] = 6.0  #  Angstrom
    units['E'] = 0.1  # kcal/mol
    units['T'] = 50.3271  # kelvin
    units['P'] = 31.755923  # atm
    return units

The "scaledpotentials" have the following scaling to get relevant units:
  --> CG factor of 6 and divide by 10 to go from Angstrom to nm
column 1 [nm]: (value)*6/10 
  --> Multiply by * 0.1 to go to kcal/mol * 4.18400 to go to kJ/mol
column 2 [kJ/mol]: (value)*0.1*4.184
  --> Like column 2 to get kJ/mol, then divide by like column 1 to get kJ/mol-nm
column 3 [kJ/mol-nm]: (value)*0.1*4.184/(6/10)

Finally, in the folder scaledplots, are the plots of the potential energies (kJ/mol) as a function of distance, r (nm).
This is similar to what is posted on the Github repo: https://github.com/PTC-CMC/muscl
However, the plots on Parashara's repo have the y-axis in kcal/mol

