from psychopy import iohub, hardware, visual
import psychopy.iohub as io

class Eyetracker:
    def __init__(self):
        self.ioConfig = {}
        self.ioConfig['eyetracker.hw.tobii.EyeTracker'] = {
        'name': 'tracker',
        'model_name': 'Tobii Pro X3-120 EPU',
        'serial_number': 'X3120-030118632525',
        'runtime_settings': {
            'sampling_rate': 120.0,
        }
    }
        self.blink_threshold = 3
        self.blink_counter = 0
    
    def config(self, win, experimentName, id):
        self.ioConfig['Keyboard'] = dict(use_keymap='psychopy')
        self.ioSession = '1'
        self.filename = (str(id) + '_' + experimentName)
        self.ioServer = io.launchHubServer(window=win, experiment_code='untitled', session_code=self.ioSession, datastore_name=self.filename, **self.ioConfig)
        self.eyetracker = self.ioServer.getDevice('tracker')
        # define target for calibration
        self.calibrationTarget = visual.TargetStim(win, 
            name='calibrationTarget',
            radius=10, fillColor='', borderColor='black', lineWidth=2.0,
            innerRadius=10, innerFillColor='green', innerBorderColor='black', innerLineWidth=2.0,
            colorSpace='rgb', units=None
        )
        # define parameters for calibration
        self.calibration = hardware.eyetracker.EyetrackerCalibration(win, 
            self.eyetracker, self.calibrationTarget,
            units=None, colorSpace='rgb',
            progressMode='time', targetDur=1.5, expandScale=1.5,
            targetLayout='FIVE_POINTS', randomisePos=True, textColor='white',
            movementAnimation=True, targetDelay=1.0
        )
        # define ET region of interest
        self.CentralRoi = visual.Circle(win,
            radius = 75, pos=(0, 0),
            fillColor = None, lineColor = 'black')
        self.trackRoi = visual.Circle(win,
            radius = 75, pos=(0, 0),
            fillColor = None, lineColor = 'white')
       
    def calibrate(self):
        self.calibration.run()

    def start_recording(self):
        self.eyetracker.setRecordingState(True)
    
    def stop_recording(self):
        self.eyetracker.setRecordingState(False)

    def get_data(self):
        print(f"Getting data from {self.name}")

    def check_position(self):
        gpos = eyetracker.getLastGazePosition()

        if isinstance(gpos, (tuple, list)):
            if self.cross.contains(gpos):
                return True
            else:
                return False
            
    def check_blink(self):
        gpos = eyetracker.getLastGazePosition()

        if gpos is None:
            self.blink_counter += 1
            if self.blink_counter >= self.blink_threshold:
                self.blink_counter = 0
                return False
        return True


# singleton
eyetracker = Eyetracker()