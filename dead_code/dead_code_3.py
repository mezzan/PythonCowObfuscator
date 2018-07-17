nnnnnnnnnn='Cow Language'
nnnnnnnnnnn=nnnnnnnnnn.split()
nnnnnnnnnnnn={}

for word in nnnnnnnnnnn:
    if word[0] not in nnnnnnnnnnnn.keys():
        nnnnnnnnnnnn[word[0]]=[]
        nnnnnnnnnnnn[word[0]].append(word)
    else:
        if word not in nnnnnnnnnnnn[word[0]] :
          nnnnnnnnnnnn[word[0]].append(word)
