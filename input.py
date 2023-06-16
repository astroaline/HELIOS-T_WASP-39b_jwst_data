import numpy as np
import os


## Constants ##
kboltz = 1.38064852e-16    # Boltzmann's constant
amu = 1.660539040e-24      # atomic mass unit
gamma = 0.57721
rjup = 7.1492e9            # equatorial radius of Jupiter
rsun = 6.9566e10           # solar radius
rearth = 6.378e8           # earth radius
pressure_probed = 1e-2     # probed pressure in bars
# pressure_cia = 1e-2      # pressure for cia in bars
# m = 2.4*amu              # assummed hydrogen-dominated atmosphere
m_water = 18.0*amu         # mean molecular mass of any molecules you want to consider
m_cyanide = 27.0*amu
m_ammonia = 17.0*amu
m_methane = 16.0*amu
m_carbon_dioxide = 44.0*amu
m_carbon_monoxide = 28.0*amu
m_sulfur_dioxide = 64.0*amu
solar_h2 = 0.5
solar_he = 0.085114

path = '/home/aline/Desktop/PhD/JWST_DATA_TEST/HELIOS-T-master_[non_isobaric]/'


## Planet Data ##
planet_name = 'WASP-39b'

g = 414
g_uperr = 62
g_loerr = 61
g_uncertainty = (g_uperr + g_loerr)/2
rstar = 0.918
rstar_uperr = 0.022
rstar_loerr = 0.019
rstar_uncertainty = (rstar_uperr + rstar_loerr)/2
r0 = 1.207              # Rp = [1.23,1.31]
r0_uncertainty = 0.13   # R0 = [1.077,1.337]

planet_path = path + '/planets/' + planet_name + '/'

wavelength_centre = np.load(planet_path + 'DATA/wavelength.npy')
wavelength_width = np.load(planet_path + 'DATA/wavelength_width.npy')
transit_depth = np.load(planet_path + 'DATA/transit_depth.npy') * 100
transit_depth_error = np.load(planet_path + 'DATA/transit_depth_error.npy') * 100


## Retrieval info ##
model_name = 'non_greycloud_CH4_CO2_CO'
approach_name = 'non_isobaric'

molecules = ['1H2-16O__POKAZATEL_e2b', '12C-1H4__YT34to10_e2b', '12C-16O2__CDSD_4000_e2b', '12C-16O__Li2015_e2b']
parameters = ['T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xco', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G']
res = 1         # resolution used for opacities
live = 1000     # live points used in nested sampling
wavenumber = True     # True if opacity given in terms of wavenumber, False if wavelength
num_levels = 200

priors = {'T': [2700, 200], 'log_xh2o': [13,-13], 'log_xnh3': [13,-13], 'log_xch4': [13,-13], 'log_xco2': [13,-13], 'log_xco': [13,-13],
          'log_xso2': [13,-13], 'log_P_cloudtop': [9,-8], 'log_P0': [4,-1], 'R0': [2*r0_uncertainty, r0-r0_uncertainty],
          'Q0': [99,1], 'a': [10,3], 'log_r_c': [6,-9], 'log_p_cia': [3,-3],'log_tau_ref': [7,-5], 'log_cloud_depth': [2,0],
          'Rstar': [2*rstar_uncertainty,rstar-rstar_uncertainty], 'G': [2*g_uncertainty,g-g_uncertainty], 'line': [5,0]}   # priors for all possible parameters

pmin = 1e-12


## Info for all possible parameters ##
molecular_name_dict = {'1H2-16O__POKAZATEL_e2b': 'water', '14N-1H3__CoYuTe_e2b': 'ammonia', '12C-1H4__YT34to10_e2b': 'methane', '12C-16O2__CDSD_4000_e2b': 'carbon_dioxide', '12C-16O__Li2015_e2b': 'carbon_monoxide', '32S-16O2__ExoAmes_e2b': 'sulfur_dioxide'}  # dictionary list of all possible molecules and corresponding names
molecular_abundance_dict = {'1H2-16O__POKAZATEL_e2b': 'log_xh2o', '14N-1H3__CoYuTe_e2b': 'log_xnh3', '12C-1H4__YT34to10_e2b': 'log_xch4', '12C-16O2__CDSD_4000_e2b': 'log_xco2', '12C-16O__Li2015_e2b': 'log_xco', '32S-16O2__ExoAmes_e2b': 'log_xso2'}  # dictionary list of all possible molecules and corresponding abundance names

parameter_dict = {'T': 1000, 'log_xh2o': 'Off', 'log_xnh3': 'Off', 'log_xch4': 'Off', 'log_xco2': 'Off', 'log_xco': 'Off', 'log_xso2': 'Off',
                  'log_P_cloudtop': 'Off', 'log_P0': 1, 'R0': r0, 'Q0': 'Off', 'a': 'Off', 'log_r_c': 'Off', 'log_p_cia': -2,
                  'log_tau_ref': 'Off', 'log_cloud_depth': 'Off', 'Rstar': rstar, 'G': g, 'line': 'Off'}    # default parameter values used if not retrieved

molecular_mass_dict = {'1H2-16O__POKAZATEL_e2b': m_water, '14N-1H3__CoYuTe_e2b': m_ammonia, '12C-1H4__YT34to10_e2b': m_methane, '12C-16O2__CDSD_4000_e2b': m_carbon_dioxide, '12C-16O__Li2015_e2b': m_carbon_monoxide, '32S-16O2__ExoAmes_e2b': m_sulfur_dioxide}   # dictionary of molecules and their mean molecular masses

wavenumber_dict = {'1H2-16O__POKAZATEL_e2b': '42000', '14N-1H3__CoYuTe_e2b': '20000', '12C-1H4__YT34to10_e2b': '12000', '12C-16O2__CDSD_4000_e2b': '09000', '12C-16O__Li2015_e2b': '22000', '32S-16O2__ExoAmes_e2b': '08000'}

pressure_array_opacities = 10**np.array([-12, -11.66, -11.33, -11, -10.66, -10.33, -10, -9.66, -9.33, -9, -8.66, -8.33,
                                         -8, -7.66, -7.33, -7, -6.66, -6.33, -6, -5.66, -5.33, -5, -4.66, -4.33, -4, -3.66,
                                         -3.33, -3, -2.66, -2.33, -2, -1.66, -1.33, -1, -0.66, -0.33, 0, 0.33, 0.66, 1.0])  # full log pressure array for opacities in bars
temperature_array = np.r_[50:700:50, 700:1500:100, 1500:3100:200]

temp_dict = {'1H2-16O__POKAZATEL_e2b': temperature_array, '14N-1H3__CoYuTe_e2b': temperature_array[:22], '12C-1H4__YT34to10_e2b': temperature_array,
             '12C-16O2__CDSD_4000_e2b': temperature_array, '12C-16O__Li2015_e2b': temperature_array, '32S-16O2__ExoAmes_e2b': temperature_array[:23]}   # temperature values for corresponding opacity tables
temperature_array_cia = np.r_[200:3025:25]          # temperature array for CIA table

opacity_path = '/media/aline/EXT_HD/OPACITIES/MOLECULES/'   # path to opacity binary files
cia_path = '/media/aline/EXT_HD/OPACITIES/CIA/HITRAN/'      # path to CIA files


planet_file = planet_name + '_' + approach_name + '_' + model_name + '_JWST_G395H_data'