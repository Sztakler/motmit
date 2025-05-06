from psychopy import hardware, visual, core
import psychopy.iohub as io
import os
from logger import logger

class Eyetracker:
    def __init__(self):
    #     self.ioConfig = {}
    #     self.ioConfig['eyetracker.hw.tobii.EyeTracker'] = {
    #     'name': 'tracker',
    #     'model_name': 'Tobii Pro X3-120 EPU',
    #     'serial_number': 'X3120-030118632525',
    #     'runtime_settings': {
    #         'sampling_rate': 120.0,
    #     }
    # }
    #     self.blink_threshold = 3
    #     self.blink_counter = 0
         pass
    
    def config(self, win, experimentName, id):
        # self.ioConfig['Keyboard'] = dict(use_keymap='psychopy')
        # self.ioSession = '1'
        # self.filename = (str(id) + '_' + experimentName)
        # self. data_directory = "data/eyetracker"
        # if not os.path.exists(self.data_directory):
        #     os.makedirs(self.data_directory)
    
        # # Full path to eyetracker data files
        # self.filename = os.path.join(self.data_directory, str(id) + '_' + experimentName)

        # self.ioServer = io.launchHubServer(window=win, experiment_code='untitled', session_code=self.ioSession, datastore_name=self.filename, **self.ioConfig)
        # self.eyetracker = self.ioServer.getDevice('tracker')
        # # define target for calibration
        # self.calibrationTarget = visual.TargetStim(win, 
        #     name='calibrationTarget',
        #     radius=10, fillColor='', borderColor='black', lineWidth=2.0,
        #     innerRadius=10, innerFillColor='green', innerBorderColor='black', innerLineWidth=2.0,
        #     colorSpace='rgb', units=None
        # )
        # # define parameters for calibration
        # self.calibration = hardware.eyetracker.EyetrackerCalibration(win, 
        #     self.eyetracker, self.calibrationTarget,
        #     units=None, colorSpace='rgb',
        #     progressMode='time', targetDur=1.5, expandScale=1.5,
        #     targetLayout='FIVE_POINTS', randomisePos=True, textColor='white',
        #     movementAnimation=True, targetDelay=1.0
        # )
        # # define ET region of interest
        # self.CentralRoi = visual.Circle(win,
        #     radius = 75, pos=(0, 0),
        #     fillColor = None, lineColor = 'black')
        # self.trackRoi = visual.Circle(win,
        #     radius = 75, pos=(0, 0),
        #     fillColor = None, lineColor = 'white')
        pass
       
    def calibrate(self):
        # self.win.mouseVisible = False
        # self.calibration.run()
        # self.win.mouseVisible = True
        pass

    def calibrate_and_start_recording(self):
        # self.win.mouseVisible = False
        # self.calibration.run()
        # self.start_recording()
        # self.win.mouseVisible = True
        pass

    def start_recording(self):
        # self.eyetracker.setRecordingState(True)
        pass
    
    def stop_recording(self):
        # self.eyetracker.setRecordingState(False)
        pass

    def get_data(self):
        # logger.info(f"Getting data from eyetracker")
        pass
    def check_position(self):
        # gpos = self.getLastGazePosition()

        # if gpos is None:
        #     logger.warning(f"Brak pozycji wzroku (None)aaaaaa gpos")
        #     core.wait(0.01)  # daj czas eyetrackerowi
        #     return False

        # logger.info(f"Gaze position: {gpos}")

        # if self.trackRoi.contains(gpos):
        #     logger.info("not moving")
        #     return True
        # else:
        #     logger.info("moved eyes")
        #     return False
        return True
            
    def check_blink(self):
        # gpos = self.getLastGazePosition()

        # if gpos is None:
        #     self.blink_counter += 1
        #     logger.info(f"brak pozycji wzroku (blink_counter={self.blink_counter})")

        #     if self.blink_counter >= self.blink_threshold:
        #         logger.warning("dużo mrugania / zgubienia wzroku")
        #         self.blink_counter = 0
        #         return False
            
        #     core.wait(0.01)
        #     return True  # jeszcze nie uznajemy za 'duży blink'
        
        # else:
        #     self.blink_counter = 0  # resetujemy licznik blinków bo mamy wzrok
        #     logger.info("not blinking")
        #     return True
        return True

    def getLastGazePosition(self):
        # gpos = self.eyetracker.getLastGazePosition()
        # return gpos
        pass

    def reset_state(self):
        # self.stop_recording()
        # core.wait(0.5)
        # self.eyetracker.flushData()
        # self.start_recording()
        # self.blink_counter = 0
        # logger.info("Eyetracker reset (with flush)")
        pass

# singleton
eyetracker = Eyetracker()
