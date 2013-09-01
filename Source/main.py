#coding:utf-8

import networkx as nx
import os
from LogProcess import LogProcess 


class Subway(object):

    def __init__(self):

        self._subway_dict = {}
        self._subway_info_dict =  {}
        self._station_dict = {}
        self._station_name_dict = {}
        
        self._graph = nx.Graph()

    def init(self , log_path , subway_path):

        self._log_handle = LogProcess(log_path)
        self._log_handle.init() 
        f = open(subway_path)
        subway_pos = 1 
        station_pos = 1 
        startid = 0
        endid = 0
        for each in f :
            if each == '\n': continue 
            each_list = each.strip().split(' ')
            if len(each_list) == 1 :
                self._subway_dict[each_list[0]] = subway_pos 
                subway_pos += 1
                startid = 0
                endid = 0
            elif len(each_list) >= 2 :

               
                id = int(each_list[0])
                station_name = ''.join(each_list[1:]) 
                if station_name not in self._station_name_dict :
                    self._station_name_dict[station_name] = id
                if id not in self._station_dict :
                    self._station_dict[id] = []
                self._station_dict[id].append(subway_pos -1 )     
                if startid == 0 :
                    startid = id
                elif  startid != 0 :
                    endid = id
                    self._graph.add_edge(startid,endid)
                    self._graph.add_edge(endid,startid)
                    startid = endid



    def work_one(self):
        
        key = '1号线'
        subway_id = self._subway_dict[key]
        count  = 0 
        for each  in self._station_dict :
            for tuple in self._station_dict[each] :
                if tuple == subway_id and len(self._station_dict[each]) >= 2:
                    count += 1
        print count
    def work_two(self):
        count = 0 
        user_info = self._log_handle._user_info 
        self._must_transfer  = []
        for each in user_info :
            tuple = user_info[each]
            in_id = int( tuple[0][2])
            out_id = int(tuple[1][2] )
            
    
            in_set = set(self._station_dict[in_id])
            out_set = set(self._station_dict[out_id])
            re = in_set & out_set  
            if len(re) ==  0 : 
                count += 1
                self._must_transfer.append( (in_id ,out_id) )
        print count
    
    def work_three(self):
         d = {}
         for each in self._must_transfer :
            if each not in d:
                d[each] = 0
            d[each] += 1
         sort=sorted(d.items(),key=lambda e:e[1],reverse=True)
         print sort[:200]
    def work_four(self):
        key = '1号线'
        subway_id = self._subway_dict[key]
        one_set = set()
        for each in self._station_dict :
            if subway_id in self._station_dict[each]:
                one_set.add(each)

        user_info = self._log_handle._user_info 
        id_in_info = {}
        for each in user_info :
            tuple = user_info[each]
            in_id = int( tuple[0][2])
            out_id = int(tuple[1][2] )

            next_id = nx.shortest_path(self._graph,source=in_id,target=out_id)[1]

            if in_id in one_set and next_id in one_set:
                if in_id not in id_in_info :
                    id_in_info[in_id] = []
                num = self.time_to_num(tuple[0][0])
                id_in_info[in_id].append(num)

        for each in id_in_info:
            self.max_count (id_in_info[each])
    
    def max_count(self , time_list ):
        time_count = [0 for pos in range(24*60*60)]
        for each in time_list :
            time_count[each] += 1
        time_sum = sum (time_count[:60])
        max_sum = time_sum 
        start_time = 0 
        end_time = 0
        for pos in range(60 , 24*60*60):
            time_sum = time_sum - time_count[pos - 60] + time_count[pos]
            if time_sum > max_sum :
                max_sum = time_sum  
                start_time = pos - 60
                end_time = pos 

        print start_time ,end_time , max_sum 
    def time_to_num(self,time):
        num_list = time.strip().split(':')
        num = int(num_list[0])*3600 + int(num_list[1])*60 + int(num_list[2])
        return num

def main():

    test = Subway()
    #test.init('../Question/sample.log','../Question/subway.txt.utf')
    test.init('../Question/subway.log','../Question/subway.txt.utf')
    test.work_one()
    test.work_two()
    test.work_four()

if __name__ == '__main__':
    main()




