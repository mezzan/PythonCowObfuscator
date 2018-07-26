def quicksort(list):
    def partition(pivot,list):
       slist = []
       glist = []
       for x in list:
           if compara(x, pivot):
               glist += [x]
           else:
               slist += [x]
       return slist, glist
    if len(list) <= 1:
        return list
    else:
        slist, glist = partition(list[0],list[1:])
        print(list[0] + slist + glist)
        return quicksort(slist) + [list[0]] + quicksort(glist)