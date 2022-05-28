import redis
import re

def read_redis (redishost, redisport, redisdb, redistimeout, key):
    redthis=redis.StrictRedis(host=redishost,port=redisport, db=redisdb, socket_timeout=redistimeout)
    try:
      get=redthis.get(key).decode("utf-8")
    except:
      print (f"Unable to get key {key} $!")
      get="Error"
    return (get)
    
def write_redis (redishost, redisport, redisdb, redistimeout, key, value, ttl):
    redthis=redis.StrictRedis(host=redishost, port=redisport, db=redisdb, socket_timeout=redistimeout)
    print (f"key={key}, value={value}, ttl={ttl}")
    try:
      set=redthis.set(key, value)
      if ttl > 0:
          setttl=redthis.expire(key,ttl)
    except:
      print (f"Unable to set key {key} $!")
      set="Error"
    return (set)
    
def ttl_redis (redishost, redisport, redisdb, redistimeout, key):
    redthis=redis.StrictRedis(host=redishost,port=redisport, db=redisdb, socket_timeout=redistimeout)
    try:
      get=int(redthis.ttl(key))
    except:
      print (f"Unable to get key {key} $!")
      get="Error"
    return (get)
