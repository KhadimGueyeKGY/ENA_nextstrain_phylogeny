import os 


class nextstrain :

    def precess(input_dir):
        os.system ('nextstrain build --cpus 1 '+input_dir)
        #os.system('cp package/zika/auspice/* auspice_res/')
    

    def view():
        os.system('nextstrain view auspice_res')
        