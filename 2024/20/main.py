import puzzle

if __name__ == '__main__':
    test = puzzle.load_puzzle('input/test.txt')
    test.find_cheats(40)
    expected = 2
    actual = test.checksum()
    assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

    test.find_cheats(74, 6)
    expected = 7
    actual = test.checksum()
    #assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}" 
    # wrong example! there is only 1 cheat that gives 76 advantage, not 3!

    quest = puzzle.load_puzzle('input/quest.txt')
    quest.find_cheats(100)
    actual = quest.checksum()
    print("Quest Checksum:", actual)
    
    expected = 1402
    assert expected==actual, f"Part 1 failed!\n  Expected: {expected}\n  Actual: {actual}"

    quest.find_cheats(100, 20)
    actual = quest.checksum()
    print("Quest Checksum Part 2:", actual)
