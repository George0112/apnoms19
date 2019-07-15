#encoding=utf-8
from multiprocessing.connection import Listener
from .transformer import Transformer 

address = ('localhost', 8888)     # family is deduced to be 'AF_INET'
listener = Listener(address)



while True:
    conn = listener.accept()
    print('connection accepted from', listener.last_accepted)
    
    T_decision = conn.recv()
    print(T_decision)
    try:
        transformer = Transformer()
        for d in S_decision:
            (c,f,a) = d
            analyst.analyze(c,f,a)
        
    except Exception as e:
        print(e)
    finally:
        conn.close()



listener.close()