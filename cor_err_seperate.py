import codecs

#the input of the function: the cor and err pair
def seperate(combined_file):
    with codecs.open(combined_file, 'r', encoding='utf8') as f:
        #1 line 1 pair
        pairs = f.readlines()
        for line in pairs:
            #some of them is seperated by
            content = line.split('\t')
            if len(content) == 2:
                correct = content