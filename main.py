__author__ = 'Khadim GUEYE - Colman'

import yaml 
import sys , os
from package.download_data import DownData
from package.nextstrain import nextstrain



def pathogens ():
    try:
        with open('pathogens.yaml', 'r') as file:
            pathogens = yaml.safe_load(file)
            West_Nile_virus = str(pathogens['West Nile virus'])
            Zika = str(pathogens['Zika'])
            return West_Nile_virus , Zika
    except FileNotFoundError:
        sys.exit()


def main():
    West_Nile_virus , Zika = pathogens ()
    #os.system('mkdir -p data/West_Nile_virus data/Zika')
    
    #----------------- West_Nile_virus ----------------------
    #DownData.downdata(West_Nile_virus, 'data/West_Nile_virus')
    #DownData.metadata_prep('data/West_Nile_virus/','package/West_Nile/data/','west nile')
    #DownData.fataprep ('data/West_Nile_virus/','package/West_Nile/data/')
    #nextstrain.precess('package/West_Nile/')


    #----------------------- Zika --------------------------
    DownData.downdata(Zika, 'data/Zika')
    #DownData.metadata_prep('data/Zika/','package/zika/data/','zika')
    #DownData.fataprep ('data/Zika/','package/zika/data/')
    #nextstrain.precess('package/zika')


    #----------------------------- view 


if __name__ == '__main__':
    main()






