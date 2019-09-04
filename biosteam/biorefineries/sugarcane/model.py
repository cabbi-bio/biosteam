# -*- coding: utf-8 -*-
"""
Created on Sun May 26 11:21:31 2019

@author: yoelr
"""
from biosteam.evaluation import Model, Metric
from biosteam.evaluation.evaluation_tools import triang
import biosteam.biorefineries.sugarcane as sc

__all__ = ('sugarcane_model',)

tea = sc.sugarcane_sys.TEA
Ethanol = sc.system.Ethanol
get_prodcost = lambda: float(tea.production_cost(Ethanol))
get_FCI = lambda: tea._FCI_cached
get_prod = lambda: Ethanol.massnet * tea._annual_factor

metrics = (Metric('Internal rate of return', '%', sc.sugarcane_tea.solve_IRR),
           Metric('Ethanol production cost', 'USD/yr', get_prodcost),
           Metric('Fixed capital investment', 'USD', get_FCI),
           Metric('Ethanol production', 'kg/hr', get_prod))

sugarcane_model = Model(sc.sugarcane_sys, metrics, skip=False)
sugarcane_model.load_default_parameters(sc.system.Sugar_cane)
param = sugarcane_model.parameter

# Fermentation efficiency
fermentation = sc.system.P24
@param(element=fermentation, distribution=triang(fermentation.efficiency),
       kind='coupled')
def set_fermentation_efficiency(efficiency):
    fermentation.efficiency= efficiency
    
# Boiler efficiency
BT = sc.system.BT
@param(element=BT, distribution=triang(BT.boiler_efficiency))
def set_boiler_efficiency(boiler_efficiency):
    BT.boiler_efficiency = boiler_efficiency

# Turbogenerator efficiency
@param(element=BT, distribution=triang(BT.turbogenerator_efficiency))
def set_turbogenerator_efficiency(turbo_generator_efficiency):
    BT.turbo_generator_efficiency = turbo_generator_efficiency
    
# RVF separation
rvf = sc.system.P14
@param(element=rvf, distribution=triang(rvf.split['Lignin']),
        kind='coupled')
def set_rvf_solids_retention(solids_retention):
    rvf.split['Lignin', 'CaO', 'Ash', 'Cellulose', 'Hemicellulose'] = solids_retention









