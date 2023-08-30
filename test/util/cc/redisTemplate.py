import redis

rediscon=redis.Redis(host='localhost',port=6379,db=0)
def setKey(key ,val):
    print("key")

def close():
    rediscon.close()