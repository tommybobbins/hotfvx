import redis
import re

def read_redis (host, port, db, socket_timeout, key):
    redthis=redis.StrictRedis(host=redishost,port=redisport, db=redisdb, socket_timeout=redistimeout)
    try:
      get=redthis.get("key")
    except:
      print (f"Unable to get key {key} $!")
      get="Error"
    return (get)
    
def write_redis (host, port, db, socket_timeout, key, value):
    redthis=redis.StrictRedis(host=redishost,port=redisport, db=redisdb, socket_timeout=redistimeout)
    try:
      set=redthis.set("key")
    except:
      print (f"Unable to set key {key} $!")
      set="Error"
    return (set)
    
