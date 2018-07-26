pppppp = ["<B>","Jack","and","Jill","</B>","went","up","the","hill","to","<B>","fetch","a","pail","of","</B>","water.","Jack","fell","<B>","down","and", "broke","</B>","his","crown","and","<B>","Jill","came","</B>","tumbling","after"]
def get_bolds(list):
        true = 1
        false = 0
        is_bold = false
        start_block = 0
        for index in range(len(list)):
                if list[index] == "<B>":
                        if is_bold:
                                print("Error:  Extra Bold")
                        is_bold = true
                        start_block = index+1
                if list[index] == "</B>":
                        if not is_bold:
                                print("Error: Extra Close Bold")
                        print("Bold ["+start_block+":"+index+"] ")
                        list[start_block:index]
                        is_bold = false
                        start_block = index+1