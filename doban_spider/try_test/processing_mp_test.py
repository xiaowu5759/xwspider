# -*- coding: utf-8 -*-
'''
@createBy  :   xiaowu 
@date    :   2019/10/22 14:16:41
'''

import multiprocessing as mp

def job(q):
    res = 0
    
    for i in range(12):
        res += i+i**2+i**3
    q.put(res)



if __name__ == "__main__":
    queue = mp.Queue()
    p1 = mp.Process(target=job,args=(queue,))
    p1.start()
    for _ in range(1000):
        if(not queue.empty()):
            print('has')
        else:
            print('emtpy')