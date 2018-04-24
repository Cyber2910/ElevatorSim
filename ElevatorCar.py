from ElevatorComponent import ElevatorComponent
from threading import Thread
from Messages import *


class ElevatorCar(ElevatorComponent):

    def __init__(self, CarCtrl, Motor, CarDoor):
        super().__init__()
        # input
        self.iCmd = None    # Received from Elevator Controller

        # output
        self.oReq = None # Recipient is Request Processor
        self.oStCar = None # Recipient is Elevator Controller
        self.oStDoor = None # Recipient is Door Status Processor

        # Instance variables to store the actual message objects that will be sent via Pipes
        self.oReqMsg = None
        self.oStCarMsg = None
        self.oStDoorMsg = None

        # Coupled Input/Output: iCmd goes to "in" on the CarCtrl so we need an instance of the CarCtrl
        self.ctrl = CarCtrl
        self.motor = Motor
        self.door = CarDoor

        
    def setoReqMsg(self, msg):
        self.oReqMsg = msg
        # Generate oReqMsg log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Car Button","Elevator Car","R", self.oReqMsg.contents)
        
        # Generate oReq log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Car","Request Proc","S", self.oReqMsg.contents)

        # Send oReq
        self.oReq.send(self.oReqMsg)

    def setoStCarMsg(self, msg):
        self.oStCarMsg = msg
        # Generate oStCarMsg log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","Elevator Car","R", self.oStCarMsg.contents)
        
        # Generate oStCar log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Car","Elevator Ctrl","S", self.oStCarMsg.contents)
                
        # Send oStCar
        self.oStCar.send(self.oStCarMsg)

    def setoStDoorMsg(self, msg):
        self.oStDoorMsg = msg
        # Generate oStDoorMsg log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","Elevator Car","R", self.oStDoorMsg.contents)
        
        
        # Generate oStDoor log
        self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Car","Door Status Proc","S", self.oStDoorMsg.contents)
               
        # Send oStDoor
        self.oStDoor.send(self.oStDoorMsg)


    def state_processor(self):
        thread_carCtrl = Thread(target = self.ctrl.state_processor, args = ())
        thread_carCtrl.start()
        
        while True:
            # Get iCmd
            try:
                job = self.iCmd.recv()
                # Generate oStCarMsg log
                self.write_log(self.get_sim_time(), self.get_real_time(),"Elevator Ctrl","Elevator Car","R", job.contents)

                self.ctrl.setIN(job)
            except EOFError:
                pass

    def main(self):
       self.state_processor()



if __name__ == '__main__':
    ctrl = None
    motor = None
    door = None
    car = ElevatorCar(ctrl, motor, door)
    car.main()