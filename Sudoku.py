
#this class will hold the data for each value... there will be 81 in total
class cell():
    def __init__(self, value, position, row = None, col = None, zone = None):
        self.value = value
        self.position = position
        
        self.row = row
        self.col = col
        self.zone = zone
        self.possible = [x for x in range(1,10)]

class Sudoku():
    def __init__(self, board):
        self.board_input = [int(char) for char in board] ## convert string to list of numbers

        #will hold all the 81 objects
        

        ## zones from 1 to 9 with their positions (1-81) in a list
        self.zone_map = {   1 : [1, 2, 3, 10, 11, 12, 19, 20, 21],
                            2 : [4, 5, 6, 13, 14, 15, 22, 23, 24],
                            3 : [7, 8, 9, 16, 17, 18, 25, 26, 27],
                            4 : [28, 29, 30, 37, 38, 39, 46, 47, 48],
                            5 : [31, 32, 33, 40, 41, 42, 49, 50, 51],
                            6 : [34, 35, 36, 43, 44, 45, 52, 53, 54],
                            7 : [55, 56, 57, 64, 65, 66, 73, 74, 75],
                            8 : [58, 59, 60, 67, 68, 69, 76, 77, 78],
                            9 : [61, 62, 63, 70, 71, 72, 79, 80 , 81]}



    def extract_data(self):

        self.board = []

        """
            position is like : 1,2,3,4...
                                .
                                .
                                ...79,80,81
        """

        list_of_obj = []

        for position, i in enumerate(self.board_input):
            value = None if i == 0 else i
            list_of_obj.append(cell(value, position+1)) #1-81

        #split into rows
        row = []
        for i in range(0,81):
            row.append(list_of_obj[i])
            if len(row) == 9:
                self.board.append(row)
                row = []
        

        ## add row, colum and zones to previously created objects
        for row in self.board:
            col_count = 1
            for ele in row:
                ele.row = row

                col_list = []
                
                for row2 in self.board:
                    col_count2 = 1
                    for ele2 in row2:
                        if col_count2 == col_count:
                            col_list.append(ele2)

                        col_count2 += 1

                ele.col = col_list

                zone = None
                
                for key, value2 in self.zone_map.items():
                    if ele.position in value2:
                        zone = key

                zone_list = []
                ## make a list of all the elements in the zone that the currrent element is in 
                for row2 in self.board:
                    for ele2 in row2:
                        if ele2.position in self.zone_map[zone]:
                            zone_list.append(ele2)
    

                ele.zone = zone_list
                
                col_count += 1

        self.rows = self.board
        self.cols = [[self.board[j][i] for j in range(len(self.board))] for i in range(len(self.board[0]))]
        self.zones = []

        for key,value in self.zone_map.items():  
            zone_temp = []
            for i in value:
                for row in self.board:
                    for x in row:
                        if x.position == i:
                            zone_temp.append(x)

            self.zones.append(zone_temp)

                
    def narrow_possibility_using_assigned(self, cell):

        if cell.value != None:
            cell.possible = [cell.value]

        for i in cell.row:
            if i.value == None:
                i.possible = [x for x in i.possible if x != cell.value]

        for i in cell.col:
            if i.value == None:
                i.possible = [x for x in i.possible if x != cell.value]

        for i in cell.zone:
            if i.value == None:
                i.possible = [x for x in i.possible if x != cell.value]

    def check_and_assign(self):
        def check(crz):
            
            if crz == "row":
                crz_obj = self.rows
                
            elif crz == "col":
                crz_obj = self.cols
                
            elif crz == "zone":
                crz_obj = self.zones

            ## remove fixed vals from possible  
            for group in crz_obj:
                for cell in group:
                    if cell.value != None:
                        continue

                    if len(cell.possible) ==1:
                        cell.value = cell.possible[0]
                        continue

                    fixed_vals = []

                    for i in cell.row:
                        if i != None:
                            fixed_vals.append(i.value)

                    for i in cell.col:
                        if i != None:
                            fixed_vals.append(i.value)

                    for i in cell.zone:
                        if i != None:
                            fixed_vals.append(i.value)

                    cell.possible = [j for j in cell.possible if j not in fixed_vals]

            ##assign if only value in the group
            for group in crz_obj:
                for cell in group:
                    if cell.value != None:
                        continue

                    possible_other = []

                    for i in cell.row:
                        if i != cell:
                            possible_other += i.possible

                    for i in cell.col:
                        if i != cell:
                            possible_other +=  i.possible

                    for i in cell.zone:
                        if i != cell:
                            possible_other +=  i.possible

                    possible = []
                    for i in cell.possible:
                        if i not in possible_other:
                            possible.append(i)
                    if len(possible) > 0:
                        cell.possible = possible


            ##assign if 1 ele in possible
            for cell in group:
                if cell.value == None:
                    if len(cell.possible) == 1:
                        cell.value = cell.possible[0]
           
        check("row")
        check("col")
        check("zone")
    


    def check_naked_pair(self):
        def pair(crz):
            crz_obj = None

            if crz == "row":
                crz_obj = self.rows
                
            elif crz == "col":
                crz_obj = self.cols
                
            elif crz == "zone":
                crz_obj = self.zones

            
            for group in crz_obj:
                found = []
                for cell in group:
                    if len(cell.possible) != 2:
                        continue

                    for cell2 in group:
                        if len(cell2.possible) != 2:
                            continue
                        

                        if cell == cell2:
                            continue
                    
                        if cell.possible == cell2.possible:
                            found.append(cell)

                
                if len(found) == 2:
                    values = found[0].possible

                    for cell in group:
                        if cell in found:
                            continue

                        for i in cell.possible:
                            if i in values:
                                return
                        
                    for x in group:
                        if x in found:
                            continue

                        x.possible = [j for j in x.possible if j not in values]
                        self.check_and_assign()

        pair("row")
        pair("col")
        pair("zone")


    def check_naked_triple(self):

        def triple(crz):
            
            crz_obj = None

            if crz == "row":
                crz_obj = self.rows
                
            elif crz == "col":
                crz_obj = self.cols
                
            elif crz == "zone":
                crz_obj = self.zones

            for group in crz_obj:
                candids = []

                for cell in group:
                    if cell.value != None or len(cell.possible) < 2 or len(cell.possible) > 3:
                        continue
                    
                    candids.append(cell)


                new_candid = []

                for cell in candids:
                    if len(cell.possible) != 3:
                        continue
                    found = []
                    for cell2 in candids:
                        if cell == cell2:
                            continue

                        if set(cell2.possible).issubset(set(cell.possible)):
                            if cell2 not in found:
                                found.append(cell2)


                    if len(found) == 2:
                        new_candid.append(cell)
                        new_candid += found
                        break

                if len(new_candid) != 3:
                    continue
                

                nums = []
                for i in new_candid:
                    nums += i.possible


                valid = True
                for i in nums:
                    if nums.count(i) < 2:
                        valid = False
                        break
                    
                if not valid:
                    continue

                    
                for cell in group:
                    if cell.value != None:
                        continue
                    if cell not in new_candid:
                        cell.possible = [j for j in cell.possible if j not in nums]
                                          
                self.check_and_assign()
           
        triple("row")
        triple("col")
        triple("zone")

    def check_naked_quad(self):
        def quad(crz):
            
            crz_obj = None

            if crz == "row":
                crz_obj = self.rows
                
            elif crz == "col":
                crz_obj = self.cols
                
            elif crz == "zone":
                crz_obj = self.zones

            for group in crz_obj:
                candids = []

                for cell in group:
                    if cell.value != None or len(cell.possible) < 2 or len(cell.possible) > 4:
                        continue
                    
                    candids.append(cell)


                new_candid = []

                for cell in candids:
                    if len(cell.possible) != 4:
                        continue
                    found = []
                    for cell2 in candids:
                        if cell == cell2:
                            continue

                        if cell2 in found:
                            continue
        
                        if set(cell2.possible).issubset(set(cell.possible)):
                            found.append(cell2)


                    if len(found) == 3:
                        new_candid.append(cell)
                        new_candid += found
                        break

                if len(new_candid) != 4:
                    continue
                
                nums = []
                for i in new_candid:
                    nums += i.possible


                valid = True
                for i in nums:
                    if nums.count(i) < 2:
                        valid = False
                        break
                    
                if not valid:
                    continue

                for cell in group:
                    if cell not in new_candid:
                        cell.possible = [j for j in cell.possible if j not in nums]

                self.check_and_assign()
              
        quad("row")
        quad("col")
        quad("zone")



    def check_pointing_triple(self):

        def p_triple(cell, crz):

            crz_obj = None

            if crz == "row":
                crz_obj = cell.row
                
            elif crz == "col":
                crz_obj = cell.col
                
            elif crz == "zone":
                crz_obj = cell.zone
            
            for i in crz_obj:
                if i.value != None or len(i.possible) == 1 :
                    continue

                obj_same_cr = []
                for x in crz_obj:
                    if x in i.zone:
                        obj_same_cr.append(x)

                value_to_remove = [x for x in range(1,10)]
                for x in obj_same_cr:
                    value_to_remove = [j for j in value_to_remove if j in x.possible]

                for x in cell.zone:
                    if x not in obj_same_cr:                
                        value_to_remove = [j for j in value_to_remove if j not in x.possible]

                
                for x in crz_obj:
                    if x not in obj_same_cr:
                        x.possible = [j for j in x.possible if j not in value_to_remove]
                    

        for row in self.board:
            for cell in row:
                if cell.value != None:
                    continue

                p_triple(cell,"row")
                p_triple(cell,"col")       


    def check_hidden_pair(self):
        def h_pair(crz):

            crz_obj = None

            if crz == "row":
                crz_obj = self.rows
                
            elif crz == "col":
                crz_obj = self.cols
                
            elif crz == "zone":
                crz_obj = self.zones

            for group in crz_obj:

                all_possible = []
                for cell in group:
                    if cell.value != None:
                        continue

                    all_possible +=  cell.possible

                nums = []
                not_nums = []
                for i in range(1,10):
                    if all_possible.count(i) < 3 and all_possible.count(i) > 0:
                        nums.append(i)
                    elif all_possible.count(i) > 2:
                        not_nums.append(i)
                    
                ignore_cells = []

                for cell in group:
                    if cell.value != None or len(cell.possible) < 2:
                        ignore_cells.append(cell)
                        
                for cell in group:
                    not_found = 0
                    for i in cell.possible:
                        if cell in ignore_cells:
                            continue
                        if i not in not_nums:
                            not_found += 1

                    if not_found == 1:
                        ignore_cells.append(cell)

                

                for cell in group:
                    if cell in ignore_cells:
                        continue

                    if len(list(set(cell.possible).intersection(not_nums))) < 1:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                    if len(list(set(cell.possible).intersection(nums))) < 2:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                if len(ignore_cells) > 7:
                    continue

                temp_num = []
                for i in nums:
                    for cell in ignore_cells:
                        if i in cell.possible:
                            temp_num.append(i)

                nums = [j for j in nums if j not in temp_num]

                max_cell = None
                max_count= 0
                for cell in group:
                    if cell in ignore_cells:
                        continue
                    
                    x = len(list(set(cell.possible).intersection(nums)))
                    if x > max_count:
                        max_count = x
                        max_cell = cell
                        
                nums = [j for j in nums if j in max_cell.possible]

                for cell in group:
                    if cell in ignore_cells:
                        continue

                    if len(list(set(cell.possible).intersection(nums))) < 2:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                if len(ignore_cells) > 7:
                    continue

                ## number shouldn't be in ignores
                temp_num = []
                for i in nums:
                    for cell in ignore_cells:
                        if i in cell.possible:
                            temp_num.append(i)

                nums = [j for j in nums if j not in temp_num]

                if len(nums) != 2:
                    continue

                candidates = []

                for cell in group:
                    if cell not in ignore_cells:
                        candidates.append(cell)

                if len(candidates) != 2:
                    continue

                for cell in candidates:

                    cell.possible = [j for j in cell.possible if j in nums]        

        h_pair("row")
        h_pair("col")
        h_pair("zone")
                            

    def check_hidden_triple(self):
        def h_triple(crz):

            crz_obj = None

            if crz == "row":
                crz_obj = self.rows
                
            elif crz == "col":
                crz_obj = self.cols
                
            elif crz == "zone":
                crz_obj = self.zones

            for group in crz_obj:

                all_possible = []
                for cell in group:
                    if cell.value != None:
                        continue

                    all_possible +=  cell.possible

                nums = []
                not_nums = []
                for i in range(1,10):
                    if all_possible.count(i) < 4 and all_possible.count(i) > 0:
                        nums.append(i)
                    elif all_possible.count(i) > 3:
                        not_nums.append(i)
                    
                ignore_cells = []

                for cell in group:
                    if cell.value != None or len(cell.possible) < 2:
                        ignore_cells.append(cell)
                        
                for cell in group:
                    not_found = 0
                    for i in cell.possible:
                        if cell in ignore_cells:
                            continue
                        if i not in not_nums:
                            not_found += 1

                    if not_found == 1:
                        ignore_cells.append(cell)

                

                for cell in group:
                    if cell in ignore_cells:
                        continue

                    if len(list(set(cell.possible).intersection(not_nums))) < 1:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                    if len(list(set(cell.possible).intersection(nums))) < 2:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                if len(ignore_cells) > 6:
                    continue

                temp_num = []
                for i in nums:
                    for cell in ignore_cells:
                        if i in cell.possible:
                            temp_num.append(i)

                nums = [j for j in nums if j not in temp_num]

                max_cell = None
                max_count= 0
                for cell in group:
                    if cell in ignore_cells:
                        continue
                    
                    x = len(list(set(cell.possible).intersection(nums)))
                    if x > max_count:
                        max_count = x
                        max_cell = cell
                        
                nums = [j for j in nums if j in max_cell.possible]

                for cell in group:
                    if cell in ignore_cells:
                        continue

                    if len(list(set(cell.possible).intersection(nums))) < 2:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                if len(ignore_cells) > 6:
                    continue

                temp_num = []
                for i in nums:
                    for cell in ignore_cells:
                        if i in cell.possible:
                            temp_num.append(i)

                nums = [j for j in nums if j not in temp_num]

                if len(nums) != 3:
                    continue

                candidates = []

                for cell in group:
                    if cell not in ignore_cells:
                        candidates.append(cell)

                if len(candidates) != 3:
                    continue

                for cell in candidates:
                    cell.possible = [j for j in cell.possible if j in nums]


        h_triple("row")
        h_triple("col")
        h_triple("zone")

    def check_hidden_quad(self):
        def h_quad(crz):

            crz_obj = None

            if crz == "row":
                crz_obj = self.rows
                
            elif crz == "col":
                crz_obj = self.cols
                
            elif crz == "zone":
                crz_obj = self.zones

            for group in crz_obj:

                all_possible = []
                for cell in group:
                    if cell.value != None:
                        continue

                    all_possible +=  cell.possible

                nums = []
                not_nums = []
                for i in range(1,10):
                    if all_possible.count(i) < 5 and all_possible.count(i) > 0:
                        nums.append(i)
                    elif all_possible.count(i) > 4:
                        not_nums.append(i)
                    
                ignore_cells = []

                for cell in group:
                    if cell.value != None or len(cell.possible) < 2:
                        ignore_cells.append(cell)
                        
                for cell in group:
                    not_found = 0
                    for i in cell.possible:
                        if cell in ignore_cells:
                            continue
                        if i not in not_nums:
                            not_found += 1

                    if not_found == 1:
                        ignore_cells.append(cell)

                

                for cell in group:
                    if cell in ignore_cells:
                        continue
                    if len(list(set(cell.possible).intersection(not_nums))) < 1:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                    if len(list(set(cell.possible).intersection(nums))) < 2:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                if len(ignore_cells) > 5:
                    continue

                temp_num = []
                for i in nums:
                    for cell in ignore_cells:
                        if i in cell.possible:
                            temp_num.append(i)

                nums = [j for j in nums if j not in temp_num]

                max_cell = None
                max_count= 0
                for cell in group:
                    if cell in ignore_cells:
                        continue
                    
                    x = len(list(set(cell.possible).intersection(nums)))
                    if x > max_count:
                        max_count = x
                        max_cell = cell
                        
                nums = [j for j in nums if j in max_cell.possible]


                for cell in group:
                    if cell in ignore_cells:
                        continue

                    if len(list(set(cell.possible).intersection(nums))) < 2:
                        if cell in ignore_cells:
                            continue
                        ignore_cells.append(cell)

                if len(ignore_cells) > 5:
                    continue

                ## number shouldn't be in ignores
                temp_num = []
                for i in nums:
                    for cell in ignore_cells:
                        if i in cell.possible:
                            temp_num.append(i)

                nums = [j for j in nums if j not in temp_num]

                if len(nums) != 4:
                    continue

                candidates = []

                for cell in group:
                    if cell not in ignore_cells:
                        candidates.append(cell)

                if len(candidates) != 4:
                    continue

                for cell in candidates:
                    cell.possible = [j for j in cell.possible if j in nums]


        h_quad("row")
        h_quad("col")
        h_quad("zone")


    def check_xwing(self):

        candidates = {}

        count = 0
        ##find group of 4 making an x
        for row in self.board:
            for cell in row:
                if cell.value != None:
                    continue

                if len(cell.possible) < 2:
                    continue

                for row2 in self.board:           
                    for cell2 in row2:
                        count += 1
                        pair = []

                        if cell2 == cell:
                            continue
                            
                        if cell2.value != None:
                            continue

                        if len(cell2.possible) < 2:
                            continue

                        if cell2 in cell.row or cell2 in cell.col:
                            continue

                        for i in cell.row:
                            if i in cell2.col:
                                if i.value != None:
                                    continue
                                
                                if len(i.possible) < 2:
                                    continue
                                
                                pair.append(i)

                        for i in cell.col:
                            if i in cell2.row:
                                if i.value != None:
                                    continue
                                
                                if len(i.possible) < 2:
                                    continue
                                
                                pair.append(i)
                                
                        if len(pair) == 2:
                            candidates.update({count: [cell,cell2, pair[0], pair[1]]})



        final_dict = {}
        final_num = None
        count = 0
        for key, value in candidates.items():
            num = [x for x in range(1,10)]
            for i in value:
                count +=1 
                for v in range(1,10):
                    if v not in i.possible:
                        num = [j for j in num if j != v]

            ##checking if element is found in respective rows
            if len(num) > 0:
                for v in num:
                    for z in value:
                        for y in z.row:
                            if y in value:
                                continue
                            if v in y.possible:
                                num = [j for j in num if j != v]
            valid = True
            for zone in self.zones:
                count = 0
                for i in value:
                    if i in zone:
                        count +=1

                if count > 1:
                    valid = False

            if valid == False:
                continue
                            
            ##using dict cuz there can be more than 1 xwing)
            if len(num) == 1:
                final_dict.update({count : [value,num[0]]})


        ##remove elements from column
        for _, value in final_dict.items():
            final_list = value[0]
            final_num = value[1]
            for x in final_list:
                for j in x.col:
                    if j in final_list:
                        continue
                    j.possible = [z for z in j.possible if z != final_num]




    def check_ywing(self):

        candidates = {}
        count = 0
        for row in self.board:
            for cell in row:
                count += 1

                if cell.value != None:
                    continue

                if len(cell.possible) != 2:
                    continue

                visible_cells = []
                visible_cells += cell.row + cell.col + cell.zone

                pivot = cell
                pincer1 = []
                pincer2 = []

                for cell2 in visible_cells:
                    if cell2 == cell:
                        continue
                    
                    if cell2.value != None:
                        continue

                    if len(cell2.possible) != 2:
                        continue

                    if pivot.possible[0] in cell2.possible:
                        pincer1.append(cell2)

                    if pivot.possible[1] in cell2.possible:
                        pincer2.append(cell2)


                new_pincer = []
                val = None
                for i in pincer1:
                    for j in pincer2:
                        if i == j:
                            continue
                        if i in j.row or i in j.col or i in j.zone:
                            continue

                        pincer1_values = [x for x in i.possible if x != pivot.possible[0]][0]
                        pincer2_values = [x for x in j.possible if x != pivot.possible[1]][0]

                        if pincer1_values == pincer2_values:
                            val = pincer1_values
                            if i not in new_pincer:
                                new_pincer.append(i)
                            if j not in new_pincer:
                                new_pincer.append(j)
                            
                if len(new_pincer) > 1:
                    candidates.update({count : [pivot,new_pincer,val]})

                
        for _,value in candidates.items():

            if len(value[1]) == 2:

                pincer1_visible = []
                pincer1_visible += value[1][0].row + value[1][0].col + value[1][0].zone
                
                pincer2_visible = []
                pincer2_visible += value[1][1].row + value[1][1].col + value[1][1].zone
        
                mutual = []

                for i in pincer1_visible:
                    if i in mutual:
                        continue
                    if i not in pincer2_visible:
                        continue
                    if i.value != None:
                        continue
                    if len(i.possible) < 2:
                        continue
                    if i == value[1][0] or i == value[0] or i == value[1][1]:
                        continue
                    
                    mutual.append(i)

                remove_count = 0
                for i in mutual:
                    x = len(i.possible)
                    i.possible = [z for z in i.possible if z != value[2]]
                    if len(i.possible) != x:
                        remove_count += 1

                if remove_count != 0:
                    return

    def check_xyzwing(self):

        candidates = {}
        count = 0
        for row in self.board:
            for cell in row:
                count += 1

                if cell.value != None:
                    continue

                if len(cell.possible) != 3:
                    continue

                visible_cells = []
                visible_cells += cell.row + cell.col + cell.zone

                pivot = cell
                possibilities = []
                list_of_possible = []
                

                for cell2 in visible_cells:
                    if cell2 == cell:
                        continue
                    
                    if cell2.value != None:
                        continue

                    if len(cell2.possible) != 2:
                        continue
                
                    if len(list(set(pivot.possible).intersection(cell2.possible))) > 0:
                        possibilities.append(cell2)

                for x in possibilities:
                    for j in x.possible:
                        list_of_possible.append(j)

                common = max(set(list_of_possible), default=0, key=list_of_possible.count)

                if list_of_possible.count(common) != 3:
                    continue

                if common not in pivot.possible:
                    continue

                new_possibilities = []

                for x in possibilities:
                    if x == pivot:
                        continue
                    
                    if common in x.possible:
                        new_possibilities.append(x)

                if len(new_possibilities) < 2:
                    return

                ##changin order of pivot possible for ease
                temp_list = [x for x in pivot.possible if x != common]
                temp_list.append(common)
                pivot.possible = temp_list

                pincer1 = []
                pincer2 = []

                for cell2 in new_possibilities:

                    if pivot.possible[0] in cell2.possible:
                        pincer1.append(cell2)

                    if pivot.possible[1] in cell2.possible:
                        pincer2.append(cell2)


                new_pincer = []
                val = None
                for i in pincer1:
                    for j in pincer2:
                        if i == j:
                            continue
                        if i in j.row or i in j.col or i in j.zone:
                            continue

                        pincer1_values = [x for x in i.possible if x != pivot.possible[0]][0]
                        pincer2_values = [x for x in j.possible if x != pivot.possible[1]][0]

                        if pincer1_values == pincer2_values:
                            val = pincer1_values
                            if i not in new_pincer:
                                new_pincer.append(i)
                            if j not in new_pincer:
                                new_pincer.append(j)
                            
                if len(new_pincer) > 1:
                    candidates.update({count : [pivot,new_pincer,val]})

                
        for _,value in candidates.items():

            if len(value[1]) == 2:

                pincer1_visible = []
                pincer1_visible += value[1][0].row + value[1][0].col + value[1][0].zone
                
                pincer2_visible = []
                pincer2_visible += value[1][1].row + value[1][1].col + value[1][1].zone
        
                mutual = []

                for i in pincer1_visible:
                    if i in mutual:
                        continue
                    if i not in pincer2_visible:
                        continue
                    if i.value != None:
                        continue
                    if len(i.possible) < 2:
                        continue
                    if i == value[1][0] or i == value[0] or i == value[1][1]:
                        continue
                    
                    mutual.append(i)
                    

                for i in mutual:
                    i.possible = [z for z in i.possible if z != value[2]]




    def check_swordfish(self):

        ##rows
        for i in range(1,10):
            candid_row = []
            all_cells = []
            for row in self.board:
                x = []
                for cell in row:
                    if cell.value != None:
                        continue
                    if len(cell.possible) < 2:
                        continue
                    if i in cell.possible:
                        x.append(cell)

                if len(x) > 1 and len(x) < 4: 
                    candid_row.append(x)
                    all_cells += x
            
            ##too keep on eleminiated rows
            def test(candid_row,all_cells):
                new_candid  = []
                all_cells_new = []
                for row in candid_row:
                    found = []
                    for cell in row:
                        for j in all_cells:
                            
                            if j in row:
                                continue
                            if cell in j.col:
                                if cell not in found:
                                    found.append(cell)

                    if len(row) == len(found):
                        new_candid.append(row)
                        all_cells_new += row

                return [new_candid,all_cells_new]

            ##have to do it twice to elimnite rows with elements that do not intersect
            func_return = test(candid_row,all_cells)
            new_candid = func_return[0]
            all_cells_new = func_return[1]

            func_return = test(new_candid,all_cells_new)
            new_candid = func_return[0]
            all_cells_new = func_return[1]

            if len(new_candid) != 3:
                continue

            found_cols = []
            for col in self.cols:
                for cell in all_cells_new:
                    if cell in col:
                        if col not in found_cols:
                            found_cols.append(col)

            if found_cols !=3:
                continue


            for cell in all_cells_new:
                for x in cell.col:
                    if x not in all_cells_new:
                        if x.value != None:
                            continue

                        if len(x.possible) < 2:
                            continue
                        
                        x.possible = [j for j in x.possible if j != i]


            self.check_and_assign()

            
        ##cols ## note cols and rows might have been mixed up in naming.. but it works fine
        for i in range(1,10):
            candid_row = []
            all_cells = []
            for row in self.cols:
                x = []
                for cell in row:
                    if cell.value != None:
                        continue
                    if len(cell.possible) < 2:
                        continue
                    if i in cell.possible:
                        x.append(cell)

                if len(x) > 1 and len(x) < 4: 
                    candid_row.append(x)
                    all_cells += x

            
            ##too keep on eleminiated rows
            def test(candid_row,all_cells):
                new_candid  = []
                all_cells_new = []
                for row in candid_row:
                    found = []
                    for cell in row:
                        for j in all_cells:
                            
                            if j in row:
                                continue
                            if cell in j.row:
                                if cell not in found:
                                    found.append(cell)

                    if len(row) == len(found):
                        new_candid.append(row)
                        all_cells_new += row

                return [new_candid,all_cells_new]

            ##have to do it twice to elimnite rows with elements that do not intersect
            func_return = test(candid_row,all_cells)
            new_candid = func_return[0]
            all_cells_new = func_return[1]

            func_return = test(new_candid,all_cells_new)
            new_candid = func_return[0]
            all_cells_new = func_return[1]

            if len(new_candid) != 3:
                continue

            found_rows = []
            for row in self.rows:
                for cell in all_cells_new:
                    if cell in row:
                        if row not in found_rows:
                            found_rows.append(row)

            if found_rows !=3:
                continue
            

            for cell in all_cells_new:
                for x in cell.row:
                    if x not in all_cells_new:
                        if x.value != None:
                            continue

                        if len(x.possible) < 2:
                            continue
                        
                        x.possible = [j for j in x.possible if j != i]

            self.check_and_assign()


    def check_jellyfish(self):

        ##rows
        for i in range(1,10):
            candid_row = []
            all_cells = []
            for row in self.board:
                x = []
                for cell in row:
                    if cell.value != None:
                        continue
                    if len(cell.possible) < 2:
                        continue
                    if i in cell.possible:
                        x.append(cell)

                if len(x) > 1 and len(x) < 5: 
                    candid_row.append(x)
                    all_cells += x
            
            ##too keep on eleminiated rows
            def test(candid_row,all_cells):
                new_candid  = []
                all_cells_new = []
                for row in candid_row:
                    found = []
                    for cell in row:
                        for j in all_cells:
                            
                            if j in row:
                                continue
                            if cell in j.col:
                                if cell not in found:
                                    found.append(cell)

                    if len(row) == len(found):
                        new_candid.append(row)
                        all_cells_new += row

                return [new_candid,all_cells_new]

            ##have to do it twice to elimnite rows with elements that do not intersect
            func_return = test(candid_row,all_cells)
            new_candid = func_return[0]
            all_cells_new = func_return[1]

            func_return = test(new_candid,all_cells_new)
            new_candid = func_return[0]
            all_cells_new = func_return[1]

            if len(new_candid) != 4:
                continue

            found_cols = []
            for col in self.cols:
                for cell in all_cells_new:
                    if cell in col:
                        if col not in found_cols:
                            found_cols.append(col)

            if found_cols !=4:
                continue


            for cell in all_cells_new:
                for x in cell.col:
                    if x not in all_cells_new:
                        if x.value != None:
                            continue

                        if len(x.possible) < 2:
                            continue
                        
                        x.possible = [j for j in x.possible if j != i]

            self.check_and_assign()

            
        ##cols ## note cols and rows might have been mixed up in naming.. but it works fine
        for i in range(1,10):
            candid_row = []
            all_cells = []
            for row in self.cols:
                x = []
                for cell in row:
                    if cell.value != None:
                        continue
                    if len(cell.possible) < 2:
                        continue
                    if i in cell.possible:
                        x.append(cell)

                if len(x) > 1 and len(x) < 5: 
                    candid_row.append(x)
                    all_cells += x
            
            ##too keep on eleminiated rows
            def test(candid_row,all_cells):
                new_candid  = []
                all_cells_new = []
                for row in candid_row:
                    found = []
                    for cell in row:
                        for j in all_cells:
                            
                            if j in row:
                                continue
                            if cell in j.row:
                                if cell not in found:
                                    found.append(cell)

                    if len(row) == len(found):
                        new_candid.append(row)
                        all_cells_new += row

                return [new_candid,all_cells_new]

            ##have to do it twice to elimnite rows with elements that do not intersect
            func_return = test(candid_row,all_cells)
            new_candid = func_return[0]
            all_cells_new = func_return[1]

            func_return = test(new_candid,all_cells_new)
            new_candid = func_return[0]
            all_cells_new = func_return[1]

            if len(new_candid) != 4:
                continue

            found_rows = []
            for row in self.rows:
                for cell in all_cells_new:
                    if cell in row:
                        if row not in found_rows:
                            found_rows.append(row)

            if found_rows !=4:
                continue
            
            for cell in all_cells_new:
                for x in cell.row:
                    if x not in all_cells_new:
                        if x.value != None:
                            continue

                        if len(x.possible) < 2:
                            continue
                        
                        x.possible = [j for j in x.possible if j != i]

            self.check_and_assign()
            
        
    def nishio(self):
        for row in self.board:
            for cell in row:
                if cell.value != None:
                    continue

                if len(cell.possible) == 2:
                    self.board_temp = self.board

                    import random

                    cell.value = random.choice(cell.possible)
                    return
                         

    def solve(self):
        self.extract_data()

        if not self.check_valid_board():
            print("incorrect board")
            return
        
 
        counter = 1
        counter2 = 0
        error_count = 0
        applied_nishio = False
        while not self.check_full():

            remaining = self.count_remaining()

            for row in self.board:
                for cell in row:
                    if cell.value == None:
                        continue
                    self.narrow_possibility_using_assigned(cell)

            self.check_and_assign()


            self.check_naked_pair()
            self.check_and_assign()
 

            self.check_naked_triple()
            self.check_and_assign()


            self.check_naked_quad()
            self.check_and_assign()


            self.check_pointing_triple()
            self.check_and_assign()


            self.check_hidden_pair()
            self.check_and_assign()


            self.check_hidden_triple()
            self.check_and_assign()


            self.check_hidden_quad()
            self.check_and_assign()

            
            self.check_xwing()
            self.check_and_assign()


            self.check_ywing() ##aka xywing
            self.check_and_assign()


            self.check_xyzwing()
            self.check_and_assign()

            
            self.check_swordfish()
            self.check_and_assign()
            
            
            self.check_jellyfish()
            self.check_and_assign()
            
            
            if self.check_board() == False:
                if error_count > 2:
                    if applied_nishio:
                        self.extract_data()
                        applied_nishio = False

                    else: 
                        return

                error_count +=1

            if self.count_remaining() >= remaining :
                counter2 += 1


            if counter2 > 5:
                self.nishio()
                applied_nishio = True

                counter2 = 0
    
            counter +=1

        final_list = []
        for row in self.board:
            for cell in row:
                final_list.append(cell.value)

        return ''.join(map(str, final_list))


    def count_remaining(self):
        count = 0
        for row in self.board:
            for cell in row:
                if cell.value == None:
                    count +=1

        return count
        
        
    #checks if the board is complete correctly
    def check_full(self):
        ## check if any cell is empty
        for row in self.board:
            for cell in row:
                if cell.value == None:
                    return False
        return True
    
    def check_valid_board(self):
        for row in self.board:
            for cell in row:
                if cell.value == None:
                    continue

                fixed_vals = []

                for i in cell.row:
                    if i == cell:
                        continue
                    if i != None:
                        fixed_vals.append(i.value)

                for i in cell.col:
                    if i == cell:
                        continue
                    if i != None:
                        fixed_vals.append(i.value)

                for i in cell.zone:
                    if i == cell:
                        continue
                    if i != None:
                        fixed_vals.append(i.value)

                if cell.value in fixed_vals:
                    return False
        return True

    def check_board(self):
        self.check_and_assign()

        def test(crz):
            
            if crz == "row":
                crz_obj = self.rows
                
            elif crz == "col":
                crz_obj = self.cols
                
            elif crz == "zone":
                crz_obj = self.zones
                
            for group in crz_obj:

                for cell in group:
                    if cell.value == None:
                        if len(cell.possible) == 0:
                            return False
                        continue
                    for cell2 in group:
                        if cell == cell2:
                            continue
                        if cell2.value == None:
                            continue

                        if cell.value == cell2.value:
                            return False

                sum = 0
                for cell in group:
                    if cell.value != None:
                        sum += cell.value

                if sum > 45:
                    return False

                
                for cell in group:
                    possibilities = []

                    for cell2 in group:
                        if cell != cell2:
                            possibilities += cell2.possible
                            
                    if cell.value in possibilities:
                         return False

            return True

        if test("row") == False:
            return False
        if test("col") == False:
            return False
        if test("zone") == False:
            return False

        return True
