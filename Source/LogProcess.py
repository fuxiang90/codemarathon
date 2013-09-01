#coding : utf-8


class LogProcess(object):

    def __init__(self,log_path):
        self._log_path = log_path

        self._user_info ={}
    def init(self):
        f = open(self._log_path)
        for line in f :
            if line[0] == '#' : continue
            l = line.strip().split(' ')
            time = l[1]
            type = l[4]
            user  = l[10]
            station_id =  l[6]
            if user not in self._user_info :
                self._user_info[user] = []
            self._user_info[user].append( (time , type ,station_id ) )

        for each in self._user_info:
            if len(self._user_info[each]) != 2 :
                print each
            

if __name__ == '__main__':

    test = LogProcess('../Question/sample.log')
    test.init()


