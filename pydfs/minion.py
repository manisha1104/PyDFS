import rpyc
import uuid

from rpyc.utils.server import ThreadedServer


class MinionService(rpyc.Service):
  class exposed_Minion():
    blocks = {}

    def exposed_put(self,block_uuid,data,minions):
      with open('/tmp/minion/'+str(block_uuid),'w') as f:
        f.write(data)
      if len(minions)>0:
        self.forward(block_uuid,data,minions)


    def exposed_get(self):
      pass   
 
    def forward(self,block_uuid,data,minions):
      print "8888: forwaring to:"
      print block_uuid, minions
      minion=minions[0]
      minions=minions[1:]
      host,port=minion.split(":")

      con=rpyc.connect(host,port=port)
      minion = con.root.Minion()
      minion.put(block_uuid,data,minions)

    def delete_block(self,uuid):
      pass

if __name__ == "__main__":
  t = ThreadedServer(MinionService, port = 8888)
  #tt = ThreadedServer(MinionService, port = 9999)
  t.start()
  #tt.start()