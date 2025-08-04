import math
import pickle as pickle

def load_bond_coeffs(system, bond_pot, picklefile, D_u, E_u):
    nb_coeffs = pickle.load(open(picklefile, 'rb'))
    bond_coeffs = nb_coeffs['bonds']
    for bond, coeffs in bond_coeffs.items():
        #bond = bytes(bond)
        try:
            alt_bond = '-'.join((bond.split('-')[1], bond.split('-')[0]))
        except IndexError:
            alt_bond = bond
        try:
            bond_pot.bond_coeff.set(bond, k=coeffs[1]*D_u**2.0/E_u, r0=coeffs[0]/D_u)
        except RuntimeError:
            pass
        try:
            bond_pot.bond_coeff.set(alt_bond, k=coeffs[1]*D_u**2.0/E_u, r0=coeffs[0]/D_u)
        except RuntimeError:
            pass
    return bond_pot

def load_angle_coeffs(system, angle_pot, picklefile, E_u):
    nb_coeffs = pickle.load(open(picklefile, 'rb'))
    angle_coeffs = nb_coeffs['angles']
    for angle, coeffs in angle_coeffs.items():
        #angle = bytes(angle)
        alt_angle = '-'.join([x for x in reversed(angle.split('-'))])
        try:
            angle_pot.angle_coeff.set(angle, k=coeffs[1]/E_u, t0=coeffs[0]*math.pi/180.0)
        except:
            pass
        try:
            angle_pot.angle_coeff.set(alt_angle, k=coeffs[1]/E_u, t0=coeffs[0]*math.pi/180.0)
        except:
            pass
    return angle_pot

def load_bonded_coeffs(system, bond_pot, angle_pot, picklefile, D_u, E_u):
    bond_pot = load_bond_coeffs(system, bond_pot, picklefile, D_u, E_u)
    angle_pot = load_angle_coeffs(system, angle_pot, picklefile, E_u)
    return bond_pot, angle_pot
