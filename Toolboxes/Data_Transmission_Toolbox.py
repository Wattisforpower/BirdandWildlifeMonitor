from serial import Serial

class TransmissionSystem:
	def __init__(self):
		pass
	
	def website(self, result):
		with open('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Toolboxes/Website/data.csv', 'a') as datafile:
			datafile.write(str(result) + "\n")
			
			datafile.close()
	
