"""
Add LabeledList and Table classes
"""

class LabeledList:
    def __init__(self, data = None, index = None):
        self.values = data
        if index == None:
            self.index = [str(i) for i in range(len(data))]
        else:
            self.index = index
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        zipped = zip(self.index,self.values)
        printable = ''
        for k,v in zipped:
            printable+= format(str(k),'<4s')
            printable+= format(str(v)+'\n','>10s')
        return printable
    def __getitem__(self,key_list):
        # declare new lists for values and index and 
        # put them into a new labledlist, and retrun this labled list.
        new_values= []
        new_index = []
        if type(key_list) == list and type(key_list[0]) != bool:
            for item in range(len(self.values)):
                if self.index[item] in key_list:
                    new_values.append(self.values[item])
                    new_index.append(self.index[item])
            return LabeledList(new_values,new_index)
        elif type(key_list[0]) == bool:
            for item in range(len(self.values)):
                if key_list[item] == True:
                    new_values.append(self.values[item])
                    new_index.append(self.index[item])
            return LabeledList(new_values,new_index)
        elif type(key_list) == str or type(key_list) == int:
            for item in range(len(self.values)):
                if key_list == self.index[item]:
                    new_values.append(self.values[item])
                    new_index.append(self.index[item])
            if len(new_index)> 1:
                return LabeledList(new_values,new_index)
            # else:
            #     return values[0]
        else:
            for item in range(len(self.values)):
                if self.index[item] in key_list.values:
                    new_values.append(self.values[item])
                    new_index.append(self.index[item])
                return LabeledList(new_values,new_index)
    def __iter__(self):
        self.n=0
        return self
    def __next__(self):
        if self.n < len(self.values):
            ret = self.values[self.n]
            self.n +=1
            return ret
        else:
            raise StopIteration

    
    def __eq__(self, scalar):
        result = [False if value == None else value ==scalar for value in self.values]
        return LabeledList(result,self.values)
    def __ne__(self, scalar):
        result = [False if value == None else value !=scalar for value in self.values]
        return LabeledList(result,self.values)
    def __gt__(self, scalar):
        result = [False if value == None else value >scalar for value in self.values]
        return LabeledList(result,self.values)
    def __lt__(self, scalar):
        result = [False if value == None else value <scalar for value in self.values]
        return LabeledList(result,self.values)
    def map(self,f):
        temp = []
        for value in self.values:
            temp.append(f(value))
        return LabeledList(temp, self.index)
    
class Table:
    def __init__(self,data,index=None,columns = None):
        self.data = data
        if index == None:
            self.index = [ i for i in range(len(data))]
        else:
            self.index = index 
        if columns ==None:
            self.columns = [ i for i in range(len(data[0]))]
        else:
            self.columns = columns
    def __str__(self):
        printable = '   '
        index = 0
        for col in self.columns:
            printable += str(col).center(15)
        printable+='\n'
        for i in self.index:
            printable += format(str(i), '<4s')
            printable += '    '.join(str(ele).center(10) for ele in self.data[index])
            printable += '\n'
            index += 1
        return printable
    def __repr__(self):
        return self.__str__()
    def __getitem__(self,col_list):
        # might need to delete these in the future
        new_col= []
        new_data=[]
        # take a labeled list and return a Table
        if type(col_list) == LabeledList:
            indexes = [i for i in range(len(self.columns)) if self.columns[i] in col_list ]
            new_col = [col for col in self.columns if col in col_list]
            for i in range(len(self.data)):
                data = []
                for j in indexes:
                    data.append(self.data[i][j])
                new_data.append(data)
            return Table(new_data,self.index,new_col)
        #using list to return a table.
        elif type(col_list) == list and type(col_list[0]) != bool:
            indexes = [self.columns.index(col_list[i]) for i in range(len(col_list)) if col_list[i] in self.columns ]
            new_col = [self.columns[col] for col in indexes]
            for i in range(len(self.data)):
                data = []
                for j in indexes:
                    data.append(self.data[i][j])
                new_data.append(data)
            return Table(new_data,self.index,new_col)
        # 3 with bool values
        elif type(col_list[0]) == bool:
            indexes = [i for i in range(len(col_list)) if col_list[i] == True]
            new_col = [self.columns[col] for col in indexes]
            for i in range(len(self.data)):
                data = []
                for j in indexes:
                    data.append(self.data[i][j])
                new_data.append(data)
            return Table(new_data,self.index,new_col)
        # 4a return 
        elif type(col_list) == str or type(col_list) == int:
            indexes = [i for i in range(len(self.columns)) if self.columns[i] == col_list]
            # print(indexes)
            new_col = [self.columns[col] for col in indexes]
            # print(new_col)
            for i in range(len(self.data)):
                data = []
                for j in indexes:
                    data.append(self.data[i][j])
                new_data.append(data)
            # print(new_data)
            if len(indexes) < 2:
                data = []
                for i in new_data:
                    for j in i:
                        data.append(j)
                return LabeledList(data,self.index)
            else:
                return Table(new_data,self.index,new_col)
    def head(self,n):
        new_head = [self.index[i] for i in range(0,n)]
        return Table(self.data,new_head,self.columns)
    def tail(self,n):
        new_tail = [self.index[i] for i in range(len(self.index)-n,len(self.index))]
        new_data = [self.data[i] for i in range(len(self.data)-n,len(self.data))]
        return Table(new_data,new_tail,self.columns)
    def shape(self):
        return (len(self.index),len(self.columns))
def read_csv(fn):
    import csv
    with open(fn,'r') as csv_data:
        csv_reader = csv.reader(csv_data, delimiter=',')
        data = [file for file in csv_reader]
    header = data.pop(0)
    return Table(data,columns=header)
        
if __name__ == '__main__':
    import nelta as nt
#    t = Table([['foo', 'bar', 'baz'],['qux', 'quxx', 'corge']])
#    print(t.index)
#    print(t.columns)
#    print(t.data)
#    print(t.shape())
    filename = '/Users/aragaom/homework02-aragaomateus/occupations-truncated.csv'
    data = nt.read_csv(filename)
    print(data.tail(4))
    levels = data['Level']
    print(levels['detail'])
    # d=[['r','w','f','g','t'],['r','w','f','g','t'],['r','w','f','g','t'],['r','w','f','g','t'],['r','w','f','g','t']]
    # t = Table(d, ['foo', 'bar', 'bazzy', 'qux', 'quxx'], ['a', 'b', 'c', 'd', 'e'])
    # print(t[LabeledList(['a', 'b'])])
    # t = Table([[15, 17, 19], [14, 16, 18]], columns=['x', 'y', 'z'])
    # print(t[[True, False, True]])
    # t = Table([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'a'])
    # print(t['a'])
    # print(nt.LabeledList([0, 1, 2, 3, 4]) > 2)