# Quaternary landscape evolution on species dispersal across Southeast Asia

This repository contains input files and pre-/post- processing notebooks and scripts to evaluate *how physiographic changes have modified the regional connectivity network and remodelled the pathways of species dispersal across Southeast Asia*. 

The approach is based on a combination of landscape evolution and connectivity models. 

## Drainage basin reorganisation and river capture

<img width="806" alt="landscape_dynamic" src="https://user-images.githubusercontent.com/7201912/119785884-fecb8780-bf12-11eb-814d-fd730c90ebcf.png">

### Notebooks

+ `1-runLEM.ipynb`: run the landscape evolution model [badlands](https://badlands.readthedocs.io/en/latest/) (forcing conditions for the landscape elevation model are provided in the `lem-models` folder), 
+ `2-getShelfInfo.ipynb`: extract information related to Sunda Shelf evolution and catchment characteristics,
+ `3-plotShelfInfo.ipynb`: plot catchment area evolution, stream parameters and Sunda Shelf information.


## Landscape connectivity for the exposed Sunda Shelf

<img width="701" alt="flow" src="https://user-images.githubusercontent.com/7201912/119787229-57e7eb00-bf14-11eb-83ce-e61b27c2abdc.png">

### Notebooks

+ `4-cptLEC.ipynb`: from landscape evolution simulation, compute the landscape elevation connectivity, 
+ `5-buildCostMap.ipynb`: to quantify the impact of geomorphology on the evolution of terrestrial biota, we build cost surface maps used in [circuitscape](https://circuitscape.org),
+ `6-getConnectivity.ipynb`: compute from circuit theory model *z-score* and *Getis-Ord index* to evaluate statistically significant connectivity hotspots between different time steps and simulations.
+ `7-plotStats.ipynb`: example of plots of statistical distribution of *landscape elevational connectivity* and *current flow* at specific time step. 

