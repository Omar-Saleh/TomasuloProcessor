from MemoryHierarchy import *
from ReservationStation import *
from InstructionBuffer import *
from ROB import *
from RegisterStatus import *

class Tomasulo(object):
	"""docstring for Tomasulo"""
	def __init__(self):
		self.reservationStations = [] 

		self.m = MemoryHierarchy("file.txt",20)
		#print(m.instructions)
		self.instructions = self.m.instructions
		self.registerStatus = RegisterStatus()
		self.ROBSize = int(input("Please enter ROB size : "))
		self.rob = ROB(self.ROBSize)
		self.pipelineWidth = int(input("Please enter pipeline width :"))
		self.bufferSize = int(input("Please enter size of instruction buffer :"))	
		self.AddUnitSize = int(input("Please enter number of ADD units : "))
		self.AddUnitCycle = int(input("Please enter number of ADD units cycles : "))
		self.MULTUnitSize = int(input("Please enter number of MULT units : "))
		self.MULTUnitCycles = int(input("Please enter number of MULT units cycles : "))
		self.LDSTUnitSize = int(input("Please enter number of LD/ST units : "))
		self.LDSTUnitCycle = int(input("Please enter number of LD/ST units cycles : "))

		for i in range(self.AddUnitSize):
			self.reservationStations.append(ReservationStation("ADD",self.AddUnitCycle))

		for i in range(self.MULTUnitSize):
			self.reservationStations.append(ReservationStation("MUL",self.MULTUnitCycles))

		for i in range(self.LDSTUnitSize):
			self.reservationStations.append(ReservationStation("LDST",self.LDSTUnitCycle))

		self.currentPC = self.m.pc
		self.instructionBuffer = InstructionBuffer(self.bufferSize)

	def fetch(self):
		for i in range(self.pipelineWidth):
			if not self.instructionBuffer.isFull() and self.currentPC in self.instructions.keys():
				self.instructionBuffer.insert(self.instructions[self.currentPC])
				if self.instructions[self.currentPC][0].lower() in self.m.parser.branchingInstructions :
					pass	
				else :
					self.currentPC += 2

	def issue(self):
		#checking rob
		if not self.rob.isFull():

			instruction = self.instructionBuffer.peek()

			if instruction in self.m.parser.addInstructions :    #check if its in the add unit
				helper("ADD")
			elif instruction in self.m.parser.mulInstructions :
				helper("MUL")
			elif instruction in self.m.parser.ldstInstructions :
				helper("LDST")

	def helper(self, s):
		for i in range(self.reservationStations): 
			if self.reservationStations[i].name == s and not self.reservationStations[i].check() :
				self.instructionBuffer.issue()
				entryNumber = self.rob.add(instruction[0],instruction[1],None)

				if self.registerStatus[instruction[2]] == None :
					readySource1 = instruction[2]
					notReadySource1 = None
				else :
					readySource1 = None
					notReadySource1 = instruction[2]

				if self.registerStatus[instruction[3]] == None :
					readySource2 = instruction[3]
					notReadySource2 = None
				else :
					readySource2 = None
					notReadySource2 = instruction[3]

				self.registerStatus[instruction[1]] = entryNumber
				if s == "LDST":
					pass
				else :
					address = None
				self.reservationStations[i].reserve(instruction[0], readySource1 , readySource2 , notReadySource1 , notReadySource2 , entryNumber , address)




t = Tomasulo()
t.fetch()
print(t.instructionBuffer.buffer)