import os 


class nextstrain :

    def precess(input_dir, virus_name):
        if virus_name =='monkeypox':
            os.system('nextstrain build --cpus 1 '+input_dir+' --configfile config/config_mpxv.yaml')
        else : 
            os.system ('nextstrain build --cpus 1 '+input_dir)
        #os.system('cp package/zika/auspice/* auspice_res/')
    

    def view():
        os.system('nextstrain view auspice_res')
        