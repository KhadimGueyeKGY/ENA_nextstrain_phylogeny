import requests, os , io
import pandas as pd 
from datetime import datetime


class DownData:
    BASE_PORTAL_API_SEARCH_URL = 'https://www.ebi.ac.uk/ena/portal/api/search'
    BASE_PORTAL_API_SEARCH_FASTA = 'https://www.ebi.ac.uk/ena/browser/api/fasta/'
    ena_searches = {
       'search_fields': ['country', 'collection_date','isolate','collected_by','first_public','host'], 'result_type': 'sequence', 'data_portal': 'ena' , 'result_type': 'sequence'
        }
    # &format=tsv
    def __init__(self):
        pass
    def get_url(taxon):
        url = ''.join([
            DownData.BASE_PORTAL_API_SEARCH_URL,
            '?',
            'dataPortal=' + DownData.ena_searches["data_portal"],
            '&',
            'fields=' + '%2C'.join(DownData.ena_searches["search_fields"]),
            '&',
            'query=tax_tree('+str(taxon)+')',
            '&',
            'result=' + DownData.ena_searches["result_type"],
            '&format=tsv&limit=0'   
        ])
        return url
    
    def downdata(taxon, output):
        url = DownData.get_url(taxon)
        response = requests.get(url)
        data = pd.read_csv(io.StringIO(response.content.decode('UTF-8')), sep="\t", low_memory=False)
        data.to_csv(output+'/metadata.tsv', sep="\t", index=False)
        accession = data['accession']
        for i in accession:
            os.system('curl "'+DownData.BASE_PORTAL_API_SEARCH_FASTA+i+'?download=true" --output '+output+'/'+i+'.fasta')
    

    def contry_to_continent(ContryInput):
        ContinentContry = pd.read_csv("package/continent_contry.txt", sep="\t")
        Continent = ContinentContry["Continent"]
        Contry = ContinentContry["Country"]
        for i in range(len(Contry)):
            if Contry[i].lower().find(ContryInput.lower()) != -1 :
                return Continent[i] , Contry[i]
        if i == len(Contry)-1 :
            return "?" , "?"
        if ContryInput.find(" ") != -1:
            CI = ContryInput.split(" ")
            for i in range(len(Contry)):
                for j in range(len(CI)):
                    if Contry[i].lower().find(CI[j].lower()) == -1 :
                        break
                if j == len(CI)-1 :
                    return Continent[i] , Contry[i]
            if i == len(Contry) -1 :
                return  "?" , "?"

    # Function to convert date format
    def convert_date(date_str):
        if date_str == 'nan':
            return 'XXXX-XX-XX'
        try:
            datetime_obj = datetime.strptime(date_str, "%b-%Y")
            return datetime_obj.strftime("%Y-%m-XX")
        except ValueError:
            try:
                datetime_obj = datetime.strptime(date_str, "%d-%b-%Y")
                return datetime_obj.strftime("%Y-%m-%d")
            except ValueError:
                try:
                    datetime_obj = datetime.strptime(date_str, "%Y")
                    return datetime_obj.strftime("%Y-XX-XX")
                except ValueError:
                    if len(date_str) == 7 and date_str[4] == '-':
                        return date_str + "-XX"
                    return date_str
    
    #-------------------- fata frep
    def fataprep(input_dir, output_dir):
        '''
        try:
            os.remove(os.path.join(output_dir, 'sequences.fasta'))
        except FileNotFoundError:
            pass
        '''
        fasta_files = [file for file in os.listdir(input_dir) if file.endswith('.fasta')]
        
        with open(os.path.join(output_dir, 'sequences.fasta'), 'w') as output:
            for fasta_file in fasta_files:
                with open(os.path.join(input_dir, fasta_file), 'r') as input_file:
                    for line in input_file:
                        if line.startswith('>'):
                            sequence_id = line.split('|')[1]
                            output.write('>' + sequence_id + '\n')
                        else:
                            output.write(line)

    #------------------------------------------- Zika and west_nilemetadata prep -----------------------------------------
    def metadata_prep(input_dir, output_dir,virus):
        data = pd.read_csv(input_dir+'/metadata.tsv', sep='\t')

        with open(output_dir+'/metadata.tsv', 'w') as output:
            if virus== 'monkeypox':
                output.write('accession\tgenbank_accession_rev\tstrain\tdate\tregion\tcountry\tdivision\tlocation\thost\tdate_submitted\tsra_accession\tabbr_authors\treverse\tclade\tlineage\tmissing_data\tdivergence\tnonACGTN\tQC_missing_data\tQC_mixed_sites\tQC_rare_mutations\tQC_frame_shifts\tQC_stop_codons\tframe_shifts\tauthors\tinstitution\n')
                for i in range(len(data)):
                    country = str(data.at[i, 'country'])
                    if country == 'nan':
                      country ='' 
                    accession = str(data.at[i, 'accession'])
                    collection_date = str(data.at[i, 'collection_date'])
                    converted_dates = DownData.convert_date(collection_date)
                    authors = str(data.at[i, 'collected_by'])
                    if authors == 'nan':
                        authors = '-'
                    first_public = str(data.at[i, 'first_public'])
                    host = str(data.at[i, 'host'])
                    if host == 'nan':
                        host = '-'
                    first_public = DownData.convert_date(first_public)
                    isolate = accession
                    if ':' in country:
                        region, ctry = DownData.contry_to_continent(country.split(':')[0])
                        division = country.split(':')[1]
                        if ',' in division:
                            city = division.split(',')[1]
                            division = country.split(',')[1]
                        else:
                            city = '?'
                    else:
                        region, ctry = DownData.contry_to_continent(country)
                        division = '?'
                        ctry = '?'
                        city = '?'

                    formatted_line = (f'{accession}\t{accession}.1\t{accession}\t{converted_dates}\t{region}\t{ctry}\t{division}\t{city}\t{host}\t{first_public}\t{accession}\t\t\t\t\t\t\t\t\t\t\t\t\t\t{authors}\t\n')
                    output.write(formatted_line)
            
            else : 
                output.write('strain\tvirus\taccession\tdate\tregion\tcountry\tdivision\tcity\tdb\tsegment\tauthors\turl\ttitle\tjournal\tpaper_url\n')
                for i in range(len(data)):
                    country = str(data.at[i, 'country'])
                    accession = str(data.at[i, 'accession'])
                    #isolate = str(data.at[i, 'isolate'])
                    collection_date = str(data.at[i, 'collection_date'])
                    authors = str(data.at[i, 'collected_by'])
                    if authors == 'nan':
                        authors = '-'
                    converted_dates = DownData.convert_date(collection_date)

                    #if isolate == 'nan':
                    isolate = accession 

                    if ':' in country:
                        region, ctry = DownData.contry_to_continent(country.split(':')[0])
                        division = country.split(':')[1]
                        if ',' in division:
                            city = division.split(',')[1]
                            division = country.split(',')[1]
                        else:
                            city = '?'
                    else:
                        region, ctry = DownData.contry_to_continent(country)
                        division = '?'
                        city = '?'

                    formatted_line = (
                        f'{isolate}\t{virus}\t{accession}\t{converted_dates}\t{region}\t{ctry}\t{division}\t{city}\tENA\tgenome\t{authors}\t'
                        f'https://www.ebi.ac.uk/ena/browser/view/{accession}\t?\t?\t?\n'
                    )
                    output.write(formatted_line)








