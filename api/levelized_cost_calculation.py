# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 21:39:53 2021

@author: Lukas Kemmer
"""

#### Levelized cost of battery cells calculator ####

import pandas as pd
import numpy as np

# Settings
pd.options.mode.chained_assignment = None  # default='warn'

def levelized_cost(construction_cost_factory,
                   lifetime_factory,
                   interest_rate,
                   tax_rate,
                   Materialkosten,
                   Materialkosten_mit_rueckgewinnung,
                   Personalkosten,
                   Energiekosten,
                   fix_cost,
                   output_kWh,
                   machine_invest,
                   factory_depreciation,
                   machine_depreciation
                   ):
        
    variable_cost = Materialkosten+Personalkosten+Personalkosten
    output_kWh = int(output_kWh)
    machine_invest = int(machine_invest)
    factory_depreciation = int(factory_depreciation)
    #factory_depreciation = int(lifetime_factory) #Assuming factory will be depreciated over its entire lifetime
    machine_depreciation = int(machine_depreciation)
    lifetime_factory = int(lifetime_factory)
    # Define variables - alle jährlich
    #construction_cost_factory = 236215.5 # Construction cost of factory -> Baukosten/Grundstück
    # lifetime_factory = 20 # Lifetime of factory -> aus Datenbank
     # Lifetime of factory -> aus Datenbank
    #interest_rate = 0.08 # Interest rate -> aus Datenbank
    #tax_rate = 0.43 # Tax rate -> kommt in Datenbank
    #variable_cost =  780634400.42 # Materialkosten, Personalkosten (ohne Overhead), Energiekosten -> Material, Personal (ohne Overhead, Personal an Maschinen, ohne 10% jeweils), Energie (Variable/Fix?) 
    #fix_cost =  654250833.22 # Fixe Personalkosten (die jeweils 10% für Führungsspanne und Reinigung etc.), Instandhaltungskosten -> alles andere, heating energie und so
    #output_kWh = 50000000 # Factory output in kWh

    #machine_invest =  541552200 # Investitionskosten für Maschinen (die alle 8 jahre neu gekauft werden müssen)
    #factory_depreciation = 20 # Zeitraum über den die Fabrik abgeschrieben wird -> in DB: Abzahlzeitraum Fabrik (weniger als Haltbarkeit Fabrik)
    #machine_depreciation = 8 # Zeitraum über den die Maschinen abgeschrieben werden (i.e. 8 Jahre weil sie alle 8 Jahre neu gekauft werden)

    ## Create dataframe


    # Create depreciation schedule based on linear depriciation
    d_i = np.full(shape=lifetime_factory+1, fill_value=0, dtype=np.float)
    d_i[1:factory_depreciation+1] = 1/factory_depreciation * construction_cost_factory # factory depreciation
    d_i[1:lifetime_factory+1] = d_i[1:lifetime_factory+1] + np.full(shape=lifetime_factory, fill_value=machine_invest/machine_depreciation, dtype=np.float)


    # Create investment array
    I_i = np.full(shape=lifetime_factory+1, fill_value=0, dtype=np.float)
    I_i[0::machine_depreciation] = machine_invest
    I_i[0] = I_i[0] + construction_cost_factory
    I_i[lifetime_factory] = 0

    # Create data frame with all parameters
    data = {
            'year' : np.arange(0,lifetime_factory+1),
            'w_i' : np.full(shape=lifetime_factory+1, fill_value=variable_cost, dtype=np.float),
            'f_i' : np.full(shape=lifetime_factory+1, fill_value=fix_cost, dtype=np.float),
            'o_i' : np.full(shape=lifetime_factory+1, fill_value=output_kWh, dtype=np.float),
            'd_i' : d_i,
            'I_i' : I_i
            }

    var_params = pd.DataFrame(data)
    # Set variable and fixed cost and output to 0 for period 0 (production starts in period 1)

    var_params['o_i'][0] = 0
    var_params['f_i'][0] = 0
    var_params['w_i'][0] = 0

    ## Calculation

    # Set gamma
    gamma = 1/(1+interest_rate)

    # Calc levelized output, o
    var_params['o_helper'] = var_params['o_i'] * np.power(gamma, var_params['year'])
    o = var_params['o_helper'].sum()

    # Calc levelized var cost, w
    var_params['v_helper'] = var_params['w_i'] * np.power(gamma, var_params['year'])
    w = var_params['v_helper'].sum() / o

    # Calc levelized fixed cost, f
    var_params['v_helper'] = var_params['f_i'] * np.power(gamma, var_params['year'])
    f = var_params['v_helper'].sum() / o

    # Calc depreciation (absolute, discounted per year)
    var_params['d_helper'] = var_params['d_i'] * np.power(gamma, var_params['year'])

    # Calc investment (absolute, discounted per year)
    var_params['I_helper'] = var_params['I_i'] * np.power(gamma, var_params['year'])

    # Calc levelized cost of battery cells (LCOB), lc_b
    lc_b = w + f + (var_params['I_helper'].sum()- tax_rate * var_params['d_helper'].sum()) / ((1-tax_rate)*o)

    # Calculate marginal cost of batteries
    mc_b = variable_cost / output_kWh

    # Calculate full cost of batteries
    fc_b = (variable_cost + fix_cost + construction_cost_factory/factory_depreciation + machine_invest / machine_depreciation) / output_kWh

    ## Output results

    #print('LCOB = ', round(lc_b, 4), ' EUR / kWh')

    #print('MC = ', round(mc_b, 4), ' EUR / kWh')

    #print('FC = ', round(fc_b, 4), ' EUR / kWh')

    full_cost_aufgeteilt = [
        {
            "group": "Material",
            "value":  Materialkosten,

        },
        {
            "group": "Personal",
            "value":  Personalkosten
        },
        {
            "group": "Energie",
            "value":  Energiekosten
        },
        {
            "group": "Abschreibung",
            "value": construction_cost_factory/factory_depreciation + machine_invest / machine_depreciation
        },
        {
            "group": "Overhead",
            "value": fix_cost
        }
    ]

    return {"levelized_cost":round(lc_b,2),"marginal_cost":round(mc_b,2), "full_cost":round(fc_b, 2)},full_cost_aufgeteilt

    # ToDo: depending on factory lifetime add remaining value of machines at end of 
    # life of factory (i.e. if not fully depreciated)
    # ToDo: checken ob man Energiekosten in variable und overhead aufteilen kann
    # falls ja sollte bei MC nur der Variable anteil rein
