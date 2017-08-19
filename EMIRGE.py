
import subprocess,os,sys
dataDir = sys.argv[1]
for folder in os.listdir(dataDir):
    if os.path.isdir(os.path.join(dataDir, folder)):
        if 'iter.00' in os.listdir(os.path.join(dataDir, folder)):
            rounds = []
            for iters in os.listdir(os.path.join(dataDir, folder)):
                if iters.startswith('iter'):
                    rounds.append(int(iters.lstrip('iter.')))
            if max(rounds) == 0:
                print('%s\t%s'%(folder,'Nothing'))
                continue
            elif max(rounds) < 10:
                lastround = '0' + str(max(rounds))
            else:
                lastround = str(max(rounds))
            cmd = "grep '>' {}/iter.{}/iter.{}.cons.fasta".format(folder,lastround,lastround)
            results = subprocess.check_output(cmd, shell = True)
            if results.count('>') == 0:
                print('%s\t%s'%(folder,'Nothing'))
            elif results.count('>') == 1:
                accession = results.split('.')[0].lstrip('>')
                #cmd = "zcat /media/backup_2tb/Data/nr_protein/accession2taxid.gz | grep {} -m 1".format(accession)
                #taxid = subprocess.check_output(cmd, shell = True)
                print('%s\t%s'%(folder,accession))
            else:
                results1 = results.split('\n')[:-1]
                for result in results1:
                    accession = result.split('.')[0].lstrip('>')
                    #cmd = "zcat /media/backup_2tb/Data/nr_protein/accession2taxid.gz | grep {} -m 1".format(accession)
                    #taxid = subprocess.check_output(cmd, shell = True)
                    print('%s\t%s'%(folder,accession))

'''I was trying to pull out taxid from accession2taxid but the one I have was for protein
for folder in os.listdir(dataDir):
    if os.path.isdir(os.path.join(dataDir, folder)):
        if 'iter.00' in os.listdir(os.path.join(dataDir, folder)):
            rounds = []
            for iters in os.listdir(os.path.join(dataDir, folder)):
                if iters != 'initial_mapping':
                    rounds.append(int(iters.lstrip('iter.')))
                cmd = "grep '>' {}/iter.{}/iter.{}.cons.fasta".format(folder,str(max(rounds)),str(max(rounds)))
                results = subprocess.check_output(cmd, shell = True)
                if results.count('>') == 0:
                    print('%s\t%s\n'.format(folder,'Empty\tEmpty'))
                elif results.count('>') == 1:
                    accession = results.split('.')[0].lstrip('>')
                    cmd = "zcat /media/backup_2tb/Data/nr_protein/accession2taxid.gz | grep {} -m 1".format(accession)
                    taxid = subprocess.check_output(cmd, shell = True)
                    print('%s\t%s\n'.format(folder,taxid))
                else:
                    for result in results:
                        accession = result.split('.')[0].lstrip('>')
                        cmd = "zcat /media/backup_2tb/Data/nr_protein/accession2taxid.gz | grep {} -m 1".format(accession)
                        taxid = subprocess.check_output(cmd, shell = True)
                        print('%s\t%s\n'.format(folder,taxid))
'''
