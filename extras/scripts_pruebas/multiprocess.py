from multiprocessing import Process, Queue
import time
def f(q):
	for i in range(0,20):
		q.put([i, None, 'hello'])
		time.sleep(1)

if __name__ == '__main__':
	q = Queue()
	p = Process(target=f, args=(q,))
	p.start()
	for i in range(0,20):
		print(q.get()[0])
		time.sleep(1)
	    # prints "[42, None, 'hello']"
	p.join()
