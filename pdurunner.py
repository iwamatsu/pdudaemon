import sqlite3
import logging
import time
from engine import PDUEngine
conn = None
c = None

class PDURunner():

    def __init__(self, config):
        #logging.basicConfig(level=config["logging_level"])
        conn = sqlite3.connect(config["dbfile"], check_same_thread = False)
        c = conn.cursor()

    def get_one(self):
        c.execute("SELECT * FROM pdu_queue ORDER BY id asc limit 1")
        res = c.fetchone()
        if res:
            id,hostname,port,request = res
            print(id, hostname, request, port)
            res = self.do_job(hostname,port,request)
            self.delete_row(id)

    def delete_row(self, id):
        print("deleting row %i" % id)
        c.execute("delete from pdu_queue where id=%i" % id)
        conn.commit()

    def do_job(self, hostname, port, request):
        pe = PDUEngine(hostname, 23)
        if request == "reboot":
            pe.driver.port_reboot(port)
        elif request == "on":
            pe.driver.port_on(port)
        elif request == "off":
            pe.driver.port_off(port)
        elif request == "delayed":
            pe.driver.port_delayed(port)
        else:
            print("Unknown request type: %s" % request)

    def run_me(self):
        print("Starting up the PDURunner")
        while 1:
            self.get_one()
            time.sleep(1)

if __name__ == "__main__":
    starter = {"logging_level": logging.DEBUG,
               "dbfile": "/var/lib/lava-pdu/pdu.db"}
    p = PDURunner(starter)
    p.run_me()