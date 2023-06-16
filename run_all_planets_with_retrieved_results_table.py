import os
import csv
import numpy as np

planet_list = ['WASP-39b']

earthlike_list = ['TRAPPIST-1d_earthlike', 'TRAPPIST-1e_earthlike', 'TRAPPIST-1f_earthlike', 'TRAPPIST-1g_earthlike']

approach_name = 'non_isobaric'

group0 = ['cloudfree', 'greycloud', 'non_greycloud', 'flat_line']

group1cf = ['cloudfree_CH4', 'cloudfree_CO2', 'cloudfree_CO', 'cloudfree_SO2']
group1gc = ['greycloud_CH4', 'greycloud_CO2', 'greycloud_CO', 'greycloud_SO2']
group1ngc = ['non_greycloud_CH4', 'non_greycloud_CO2', 'non_greycloud_CO', 'non_greycloud_SO2']
group1 = group1cf + group1gc + group1ngc

group2cf = ['cloudfree_CH4_CO2', 'cloudfree_CH4_CO', 'cloudfree_CH4_SO2', 'cloudfree_CO2_CO', 'cloudfree_CO2_SO2', 'cloudfree_CO_SO2']
group2gc = ['greycloud_CH4_CO2', 'greycloud_CH4_CO', 'greycloud_CH4_SO2', 'greycloud_CO2_CO', 'greycloud_CO2_SO2', 'greycloud_CO_SO2']
group2ngc = ['non_greycloud_CH4_CO2', 'non_greycloud_CH4_CO', 'non_greycloud_CH4_SO2', 'non_greycloud_CO2_CO', 'non_greycloud_CO2_SO2', 'non_greycloud_CO_SO2']
group2 = group2cf + group2gc + group2ngc

group3cf = ['cloudfree_CH4_CO2_CO', 'cloudfree_CH4_CO2_SO2', 'cloudfree_CH4_CO_SO2', 'cloudfree_CO2_CO_SO2']
group3gc = ['greycloud_CH4_CO2_CO', 'greycloud_CH4_CO2_SO2', 'greycloud_CH4_CO_SO2', 'greycloud_CO2_CO_SO2']
group3ngc = ['non_greycloud_CH4_CO2_CO', 'non_greycloud_CH4_CO2_SO2', 'non_greycloud_CH4_CO_SO2', 'non_greycloud_CO2_CO_SO2']
group3 = group3cf + group3gc + group3ngc

group4cf = ['cloudfree_CH4_CO2_CO_SO2']
group4gc = ['greycloud_CH4_CO2_CO_SO2']
group4ngc = ['non_greycloud_CH4_CO2_CO_SO2']
group4 = group4cf + group4gc + group4ngc

model_list = ['non_greycloud_CO2_CO', 'non_greycloud_CO2_CO_SO2', 'non_greycloud_CH4_CO2_CO', 'non_greycloud_CH4_CO2_CO_SO2']  #+ group1 + group2 + group3 + group4

parameter_list = ['T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xco', 'log_xso2', 'log_P_cloudtop', 'log_P0', 'R0', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_p_cia', 'log_cloud_depth', 'Rstar', 'G', 'line']

parameter_err_list = []
for p in parameter_list:
    parameter_err_list.append(p)
    parameter_err_list.append(p + '_uperr')
    parameter_err_list.append(p + '_loerr')

H2O_str = "'1H2-16O__POKAZATEL_e2b'"
NH3_str = "'14N-1H3__CoYuTe_e2b'"
CH4_str = "'12C-1H4__YT34to10_e2b'"
CO2_str = "'12C-16O2__CDSD_4000_e2b'"
CO_str = "'12C-16O__Li2015_e2b'"
SO2_str = "'32S-16O2__ExoAmes_e2b'"

molecules_dict = {'cloudfree': H2O_str,   ## cloud free
                  'cloudfree_CH4': H2O_str + ', ' + CH4_str,
                  'cloudfree_CO2': H2O_str + ', ' + CO2_str,
                  'cloudfree_CO': H2O_str + ', ' + CO_str,
                  'cloudfree_SO2': H2O_str + ', ' + SO2_str,
                  'cloudfree_CH4_CO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str,
                  'cloudfree_CH4_CO': H2O_str + ', ' + CH4_str + ', ' + CO_str,
                  'cloudfree_CH4_SO2': H2O_str + ', ' + CH4_str + ', ' + SO2_str,
                  'cloudfree_CO2_CO': H2O_str + ', ' + CO2_str + ', ' + CO_str,
                  'cloudfree_CO2_SO2': H2O_str + ', ' + CO2_str + ', ' + SO2_str,
                  'cloudfree_CO_SO2': H2O_str + ', ' + CO_str + ', ' + SO2_str,
                  'cloudfree_CH4_CO2_CO': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + CO_str,
                  'cloudfree_CH4_CO2_SO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + SO2_str,
                  'cloudfree_CH4_CO_SO2': H2O_str + ', ' + CH4_str + ', ' + CO_str + ', ' + SO2_str,
                  'cloudfree_CO2_CO_SO2': H2O_str + ', ' + CO2_str + ', ' + CO_str + ', ' + SO2_str,
                  'cloudfree_CH4_CO2_CO_SO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + CO_str + ', ' + SO2_str,
                  'greycloud': H2O_str,   ## grey cloud
                  'greycloud_CH4': H2O_str + ', ' + CH4_str,
                  'greycloud_CO2': H2O_str + ', ' + CO2_str,
                  'greycloud_CO': H2O_str + ', ' + CO_str,
                  'greycloud_SO2': H2O_str + ', ' + SO2_str,
                  'greycloud_CH4_CO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str,
                  'greycloud_CH4_CO': H2O_str + ', ' + CH4_str + ', ' + CO_str,
                  'greycloud_CH4_SO2': H2O_str + ', ' + CH4_str + ', ' + SO2_str,
                  'greycloud_CO2_CO': H2O_str + ', ' + CO2_str + ', ' + CO_str,
                  'greycloud_CO2_SO2': H2O_str + ', ' + CO2_str + ', ' + SO2_str,
                  'greycloud_CO_SO2': H2O_str + ', ' + CO_str + ', ' + SO2_str,
                  'greycloud_CH4_CO2_CO': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + CO_str,
                  'greycloud_CH4_CO2_SO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + SO2_str,
                  'greycloud_CH4_CO_SO2': H2O_str + ', ' + CH4_str + ', ' + CO_str + ', ' + SO2_str,
                  'greycloud_CO2_CO_SO2': H2O_str + ', ' + CO2_str + ', ' + CO_str + ', ' + SO2_str,
                  'greycloud_CH4_CO2_CO_SO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + CO_str + ', ' + SO2_str,
                  'non_greycloud': H2O_str,   ## non-grey cloud
                  'non_greycloud_CH4': H2O_str + ', ' + CH4_str,
                  'non_greycloud_CO2': H2O_str + ', ' + CO2_str,
                  'non_greycloud_CO': H2O_str + ', ' + CO_str,
                  'non_greycloud_SO2': H2O_str + ', ' + SO2_str,
                  'non_greycloud_CH4_CO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str,
                  'non_greycloud_CH4_CO': H2O_str + ', ' + CH4_str + ', ' + CO_str,
                  'non_greycloud_CH4_SO2': H2O_str + ', ' + CH4_str + ', ' + SO2_str,
                  'non_greycloud_CO2_CO': H2O_str + ', ' + CO2_str + ', ' + CO_str,
                  'non_greycloud_CO2_SO2': H2O_str + ', ' + CO2_str + ', ' + SO2_str,
                  'non_greycloud_CO_SO2': H2O_str + ', ' + CO_str + ', ' + SO2_str,
                  'non_greycloud_CH4_CO2_CO': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + CO_str,
                  'non_greycloud_CH4_CO2_SO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + SO2_str,
                  'non_greycloud_CH4_CO_SO2': H2O_str + ', ' + CH4_str + ', ' + CO_str + ', ' + SO2_str,
                  'non_greycloud_CO2_CO_SO2': H2O_str + ', ' + CO2_str + ', ' + CO_str + ', ' + SO2_str,
                  'non_greycloud_CH4_CO2_CO_SO2': H2O_str + ', ' + CH4_str + ', ' + CO2_str + ', ' + CO_str + ', ' + SO2_str,
                  'flat_line': H2O_str}

parameters_dict = {'cloudfree': "'T', 'log_xh2o', 'R0', 'Rstar', 'G'",   ## cloud free
                   'cloudfree_CH4':  "'T', 'log_xh2o', 'log_xch4', 'R0', 'Rstar', 'G'",
                   'cloudfree_CO2':  "'T', 'log_xh2o', 'log_xco2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CO':  "'T', 'log_xh2o', 'log_xco', 'R0', 'Rstar', 'G'",
                   'cloudfree_SO2':  "'T', 'log_xh2o', 'log_xso2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CH4_CO2':  "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CH4_CO':  "'T', 'log_xh2o', 'log_xch4', 'log_xco', 'R0', 'Rstar', 'G'",
                   'cloudfree_CH4_SO2':  "'T', 'log_xh2o', 'log_xch4', 'log_xso2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CO2_CO':  "'T', 'log_xh2o', 'log_xco2', 'log_xco', 'R0', 'Rstar', 'G'",
                   'cloudfree_CO2_SO2':  "'T', 'log_xh2o', 'log_xco2', 'log_xso2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CO_SO2':  "'T', 'log_xh2o', 'log_xco', 'log_xso2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CH4_CO2_CO':  "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xco', 'R0', 'Rstar', 'G'",
                   'cloudfree_CH4_CO2_SO2':  "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xso2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CH4_CO_SO2':  "'T', 'log_xh2o', 'log_xch4', 'log_xco', 'log_xso2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CO2_CO_SO2':  "'T', 'log_xh2o', 'log_xco2', 'log_xco', 'log_xso2', 'R0', 'Rstar', 'G'",
                   'cloudfree_CH4_CO2_CO_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xco', 'log_xso2', 'R0', 'Rstar', 'G'",
                   'greycloud': "'T', 'log_xh2o', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",   ## grey cloud
                   'greycloud_CH4': "'T', 'log_xh2o', 'log_xch4', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CO2': "'T', 'log_xh2o', 'log_xco2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CO': "'T', 'log_xh2o', 'log_xco', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_SO2': "'T', 'log_xh2o', 'log_xso2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CH4_CO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CH4_CO': "'T', 'log_xh2o', 'log_xch4', 'log_xco', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CH4_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xso2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CO2_CO': "'T', 'log_xh2o', 'log_xco2', 'log_xco', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CO2_SO2': "'T', 'log_xh2o', 'log_xco2', 'log_xso2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CO_SO2': "'T', 'log_xh2o', 'log_xco', 'log_xso2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CH4_CO2_CO': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xco', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CH4_CO2_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xso2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CH4_CO_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco', 'log_xso2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CO2_CO_SO2': "'T', 'log_xh2o', 'log_xco2', 'log_xco', 'log_xso2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'greycloud_CH4_CO2_CO_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xco', 'log_xso2', 'log_P_cloudtop', 'R0', 'Rstar', 'G'",
                   'non_greycloud': "'T', 'log_xh2o', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",   ## non-grey cloud
                   'non_greycloud_CH4': "'T', 'log_xh2o', 'log_xch4', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CO2': "'T', 'log_xh2o', 'log_xco2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CO': "'T', 'log_xh2o', 'log_xco', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_SO2': "'T', 'log_xh2o', 'log_xso2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CH4_CO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CH4_CO': "'T', 'log_xh2o', 'log_xch4', 'log_xco', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CH4_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xso2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CO2_CO': "'T', 'log_xh2o', 'log_xco2', 'log_xco', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CO2_SO2': "'T', 'log_xh2o', 'log_xco2', 'log_xso2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CO_SO2': "'T', 'log_xh2o', 'log_xco', 'log_xso2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth',  'R0', 'Rstar', 'G'",
                   'non_greycloud_CH4_CO2_CO': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xco', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CH4_CO2_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xso2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CH4_CO_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco', 'log_xso2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CO2_CO_SO2': "'T', 'log_xh2o', 'log_xco2', 'log_xco', 'log_xso2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'non_greycloud_CH4_CO2_CO_SO2': "'T', 'log_xh2o', 'log_xch4', 'log_xco2', 'log_xco', 'log_xso2', 'log_tau_ref', 'Q0', 'a', 'log_r_c', 'log_P_cloudtop', 'log_cloud_depth', 'R0', 'Rstar', 'G'",
                   'flat_line': "'line'"}

results_dict = {}

path = os.getenv('PWD') + '/'


for planet in planet_list:
    input_path = path + 'inputs/'
    planet_path = path + 'planets/' + planet + '/'

    ## make input file ##
    if planet in earthlike_list:
        with open(input_path + 'input_constants_earthlike.py', 'r') as f:
            constants = f.read()
    else:
        with open(input_path + 'input_constants_H2.py', 'r') as f:
            constants = f.read()

    with open(planet_path + planet + '_data.py', 'r') as f:
        planet_data = f.read()

    with open(input_path + 'input_retrieval_info.py', 'r') as f:
        retrieval_info = f.read()

    with open(input_path + 'input_parameters_info.py', 'r') as f:
        parameters_info = f.read()

    for model in model_list:
        model_str = 'model_name = ' + "'" + model + "'"
        approach_str = 'approach_name = ' + "'" + approach_name + "'"
        molecules_str = 'molecules = [' + molecules_dict[model] + ']'
        parameters_str = 'parameters = [' + parameters_dict[model] + ']'

        with open(path + 'input.py', 'w') as j:
            j.write('import numpy as np' + '\n' + 'import os' + '\n\n\n')
            j.write(constants + '\n')
            j.write('path = ' + "'" + path + "'" + '\n\n\n')
            j.write(planet_data + '\n\n')
            j.write('## Retrieval info ##' + '\n')
            j.write(model_str + '\n' + approach_str + '\n\n')
            j.write(molecules_str + '\n' + parameters_str + '\n')
            j.write(retrieval_info + '\n\n')
            j.write(parameters_info + '\n\n')
            j.write('planet_file = planet_name + '"'_'"' + approach_name + '"'_'"' + model_name + '"'_JWST_G395H_data'"'')   ### change planet_file according to test

        ## run helios-t ##
        os.system('python helios-t.py')


    ## find retrieved results ##
    for model in model_list:

        with open(planet_path + 'RETRIEVED RESULTS/retrieved_results_' + planet + '_' + approach_name + '_' + model + '_JWST_G395H_data.txt', 'r') as f:
            data = f.readlines()

            row = [model]

            for param in parameter_list:

                for i in range(0, len(data)):
                    line = data[i]
                    line = line.rstrip()   # remove '\n' at end of line
                    line_list = line.split(' ')

                    if param in line_list:
                        p = [param, float(line_list[2]), float(line_list[4]), float(line_list[6])]

                if param in p:
                    for i in p[1:]:
                        row.append(i)
                else:
                    for i in 3*['-']:
                        row.append(i)

            if 'Z' in line_list:
                row.append(float(line_list[5]))

        results_dict[model] = row


    ## make retrieved results table ##
    with open(planet_path + 'results_table_' + planet + '_' + approach_name + '_JWST_G395H_data.csv', 'w', encoding='UTF8', newline='') as g:
        writer = csv.writer(g, delimiter=' ')

        header = [planet]

        for p in parameter_err_list:
            header.append(p)

        header.append('log_Z')
        writer.writerow(header)

        for model in model_list:
            writer.writerow(results_dict[model])
