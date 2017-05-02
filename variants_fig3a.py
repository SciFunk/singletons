import gzip
import sys
import math

pop_locations = open('pop_locations.txt', 'r')
###pop_locations = open('C:\\Users\\SciFunk\\Downloads\\pop_locations.txt', 'r')
sample_info = {}
for line in pop_locations:
  spline = line.split()
  sample_info[spline[0]] = spline[1:] #can use 1:3 if you only want pos 1:3 as values

def variants_to_blank_dict(samplenames, variants):
  pairs_dict = dict(zip(samplenames, variants))
  entriesToRemove = ('#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT')
  for k in entriesToRemove:
      pairs_dict.pop(k, None)
  blank_dict = {'ESN': 0, 'GWD': 0, 'LWK': 0, 'MSL': 0, 'YRI': 0, 'ACB': 0, 'ASW': 0, 'CLM': 0,
        'MXL': 0, 'PEL': 0, 'PUR': 0, 'CDX': 0, 'CHB': 0, 'CHS': 0, 'JPT': 0, 'KHV': 0,
        'CEU': 0, 'GBR': 0, 'FIN': 0, 'IBS': 0, 'TSI': 0, 'BEB': 0, 'GIH': 0, 'ITU': 0,
        'PJL': 0, 'STU': 0}
  for keys in pairs_dict.keys():  # pairs_dict.keys = list of the keys in pairs_dict
    entry1 = pairs_dict[keys]     #number of variants
    entry2 = sample_info[keys]    #['GBR', 'EUR', 'female']
    pop = entry2[0]
    try:
        blank_dict[pop] += float(entry1)
    except KeyError:
         blank_dict[pop] = entry1
  return(blank_dict)

pop_percents = {'ESN': 5,'GWD': 5,'LWK': 5,'MSL': 4,'YRI': 5,'ACB': 5,
              'ASW': 3,'CLM': 4,'MXL': 3,'PEL': 4,'PUR': 5,'CDX': 4,
              'CHB': 5,'CHS': 5,'JPT': 5,'KHV': 5,'CEU': 5,'GBR': 4,
              'FIN': 5,'IBS': 5,'TSI': 5,'BEB': 4,'GIH': 5,'ITU': 5,
              'PJL': 5,'STU': 5}

samplenames = [] #a list of samplenames format ['HG00102', 'HG00103', 'HG00105',...]
final_dict = {'ESN': 0, 'GWD': 0, 'LWK': 0, 'MSL': 0, 'YRI': 0, 'ACB': 0, 'ASW': 0, 'CLM': 0,
      'MXL': 0, 'PEL': 0, 'PUR': 0, 'CDX': 0, 'CHB': 0, 'CHS': 0, 'JPT': 0, 'KHV': 0,
      'CEU': 0, 'GBR': 0, 'FIN': 0, 'IBS': 0, 'TSI': 0, 'BEB': 0, 'GIH': 0, 'ITU': 0,
      'PJL': 0, 'STU': 0}

with gzip.open(sys.argv[1]) as data: #instead of data = gzip.open((sys.argv[1]),"rb"), this will read file line-by-line
###with gzip.open('C:\\Users\\SciFunk\\Downloads\\chr1small.vcf.gz') as data:
    for line in data:
      if line.startswith('##'): #skip all ~250 comment lines
          continue
      elif line.startswith('#'): #extract line with sample information
          samplenames = line.split()
      else:
        spline = line.split()
        x = spline.count("0|1")
        y = spline.count("1|0")
        z = spline.count("1|1")
        positions = []
        if x + y + 2*z < 25:
            for i,j in enumerate(spline): #i is the index of the element, j is the element itself
              if j == '0|1':
                positions.append(i)
              if j == '1|0':
                positions.append(i)
              if j == '1|1':
                positions.append(i)
            variants = len(samplenames)*[0]
            for i in positions:
              variants[i] += 1
            blank_dict = variants_to_blank_dict(samplenames, variants)
            for key in blank_dict:
                if blank_dict[key] >= pop_percents[key]:
                    final_dict[key] += 1
                    print key
                    print "blank_dict:", blank_dict[key]
                    print "final_dict:", final_dict[key]
print final_dict
def writeDict(dict, filename, sep):
    with open(filename, "w") as f:
        for i in dict.keys():
            f.write(i + " " + str(dict[i]) + "\n")
def readDict(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            values = line.split(sep)
            dict[values[0]] = int(values[1])
        return(dict)

dict2 = readDict("variants_fig3a.txt"," ")
for keys in dict2.keys():
  dict2[keys] += final_dict[keys]
writeDict(dict2,"variants_fig3a.txt"," ")
