from puzzle import ChronospatialPC

test = ChronospatialPC([0,1,5,4,3,0], 729)
test.do()
expected = "4,6,3,5,6,3,5,2,1,0"
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = ChronospatialPC([2,4,1,5,7,5,1,6,0,3,4,1,5,5,3,0], 44374556)
quest.do()
actual = quest.checksum()
print("Quest Checksum:", actual)

regA = quest.fixRegA(15000000)
print("Quest fixed Reg A:", regA)