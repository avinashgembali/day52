from instagram import InstaFollower
import time

obj = InstaFollower()

obj.login()
time.sleep(5)
obj.find_followers()
obj.follow()