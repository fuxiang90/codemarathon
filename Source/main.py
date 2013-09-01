#coding:utf-8
import networkx as nx
import os
import  argparse
from LogProcess import LogProcess 


class Subway(object):

    def __init__(self,type,log_path ,subway_path):

        self._subway_dict = {}
        self._subway_info_dict =  {}
        self._station_dict = {}
        self._station_name_dict = {}
        
        self._graph = nx.Graph()

        self._output = ''
        if type == 'Sample':
            self._output = 'SampleResult'
        else :
            self._output = 'Result'
        self._home = os.environ['CODEHOME']

        self._output  = os.path.join( self._home ,self._output)
        self._log_path = os.path.join( self._home ,log_path )
        self._subway_path = os.path.join(self._home , subway_path) 
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
        filename = os.path.join(self._output ,'output1.txt')
        f = open(filename,'w')
        
        f.write(str(count) + '\n')
        f.close()

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
        filename = os.path.join(self._output ,'output2.txt')
        f = open(filename,'w')
        
        f.write(str(count) + '\n')
        f.close()
    
    def work_three(self):
        d = {}
        count = 0 
        for each in self._must_transfer :
           if each not in d:
               d[each] = 0
           count += 1
           d[each] += 1
        sort=sorted(d.items(),key=lambda e:e[1],reverse=True)
        count = count - sort[0][1]
        filename = os.path.join(self._output ,'output3.txt')
        f = open(filename,'w')
        
        f.write(str(count) + '\n')
        f.close()

         
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
        
        time_max_list = []

        for each in id_in_info:
            time_tuple , max_time = self.max_count (id_in_info[each])
            time_max_list.append( (time_tuple , max_time ))
        print time_max_list
        start_time = 0
        end_time = 0 
        max_time = 0
        for each in time_max_list :
            if max_time < each[1] :
                start_time = each[0][0]
                end_time = each[0][1]
                max_time = each[1]

        filename = os.path.join(self._output ,'output4.txt')
        f = open(filename,'w')
        f.write(str(max_time) + '\n')
        f.write(self.num_to_time(start_time) +' ' + self.num_to_time(end_time) + '\n' ) 
        f.close()
    
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

        return (start_time ,end_time) , max_sum

    def num_to_time(self,num):
        s =  '%2d:%2d:%2d' %(num/3600 ,num%3600/60 ,num%60   )
        return s
    def time_to_num(self,time):
        num_list = time.strip().split(':')
        num = int(num_list[0])*3600 + int(num_list[1])*60 + int(num_list[2])
        return num
    
    def run(self):
       

        self.init(self._log_path ,self._subway_path)
        self.work_one()
        self.work_two()
        self.work_three()
        self.work_four()
        
def main():
    parser = argparse.ArgumentParser(description='Controls.',
                                     formatter_class=argparse.
                                     ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--logFile',
                        default='Question/subway.log',
                        help="subway log")
    parser.add_argument('-s', '--subWay',
                        default='Question/subway.txt',
                        help="subway txt")
    parser.add_argument('-m', '--mode', default='full', help="run mode")
    args = parser.parse_args()
    type = args.mode
    log_path = args.logFile
    subway_path = args.subWay

    test = Subway(type,log_path ,subway_path)
    test.run()
    #test.init('../Question/subway.log','../Question/subway.txt.utf')

if __name__ == '__main__':
    main()




