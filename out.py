import yaml


class OutputFormatter:
    def __init__(self, output) -> None:
        pass

    def _preformatOutput(self, rawOutputList: list) -> list:
        preformattedOutputList = []
        lineIndex = 0
        if rawOutputList[-1] == "":
            rawOutputList.pop(-1)

        if len(rawOutputList) == 1:
            return rawOutputList

        for line in rawOutputList:
            lineInfoList = []

            spaceLenght = len(line) - len(line.lstrip(" "))
            if line.lstrip(" ") != "":
                lineIndex += 1
                if not preformattedOutputList:
                    lineInfoList.extend([line.lstrip(" "), spaceLenght, lineIndex])
                elif len(preformattedOutputList) >= 1 and lineIndex != len(
                    rawOutputList
                ):
                    preformattedOutputList[-1].append(spaceLenght)
                    lineInfoList.extend([line.lstrip(" "), spaceLenght, lineIndex])
                elif lineIndex == len(rawOutputList):
                    preformattedOutputList[-1].append(spaceLenght)
                    lineInfoList.extend([line.lstrip(" "), spaceLenght, lineIndex, 0])
                else:
                    pass

                preformattedOutputList.append(lineInfoList)
            else:
                pass
        return preformattedOutputList

    def _getOutputStats(self, outputList: list) -> dict:
        """
        This function calculates number of lines for each number of spaces at the start of line.
        """
        spaceCountDict = {}
        for lineInfo in outputList:
            currentSpaceCount = str(lineInfo[1]) + "_space_count"
            if not spaceCountDict:
                spaceCountDict[currentSpaceCount] = "1"
            else:
                for key, value in spaceCountDict.copy().items():
                    if key == currentSpaceCount:
                        spaceCountDict[key] = str(int(value) + 1)
                        break
                    elif (
                        key != currentSpaceCount
                        and key != list(spaceCountDict.keys())[-1]
                    ):
                        pass
                    else:
                        spaceCountDict[currentSpaceCount] = "1"
                        break
        return spaceCountDict

    def _getTreeDepth(self, spaceCountDict: dict) -> int:
        depth = 0
        for key in spaceCountDict.keys():
            depth += 1
        return depth

    def _createDepthInfoDict(self, spaceCountDict) -> dict:
        treeDepthDict = {}
        treeDepth = self._getTreeDepth(spaceCountDict)
        for i in range(treeDepth, 0, -1):
            depth = "depth_" + str(i)
            treeDepthDict[depth] = 1
        treeDepthDict = dict(reversed(list(treeDepthDict.items())))
        return treeDepthDict

    def _increaseMultiplier(self, treeDepthDict) -> int:
        spaceMiltiplier = 0
        prevDepth = 1
        isFirst = True
        for count in treeDepthDict.values():
            if (isFirst and count == 0) or (count == 0 and prevDepth == 0):
                prevDepth = count
                spaceMiltiplier += 1
            elif count == 1 and prevDepth == 0:
                break
            else:
                pass
            isFirst = False
        return spaceMiltiplier

    def _checkAndSetsetSpaceMultiplier(self, spaceMiltiplier, currentDepth):
        if spaceMiltiplier > currentDepth:
            spaceMiltiplier = currentDepth
        if currentDepth - spaceMiltiplier == 0:
            spaceMiltiplier -= 1
        return spaceMiltiplier

    def output(self, output):
        # Convert class tree to yaml
        outputLine = str(yaml.dump(output))
        # Create list by spliting string by new line
        rawOutputList = outputLine.split("\n")
        # Create list of lists, which contains class name, current amount of spaces, index, and amount of spaces at next line
        preformattedOutputList = self._preformatOutput(rawOutputList)
        # Create dict which contains number of strings with each amount of spaces
        spaceCountDict = self._getOutputStats(preformattedOutputList)
        # Create dict to indicating depth of class tree
        treeDepthDict = self._createDepthInfoDict(spaceCountDict)

        # Check of input contain only one string, and return in as output
        if len(preformattedOutputList) == 1:
            print(preformattedOutputList[0])
            return

        for lineInfo in preformattedOutputList:
            currentLineSpace = int(lineInfo[1])
            nextLineSpace = int(lineInfo[3])
            currentDepth = round(currentLineSpace / 2)
            nextSpaceCount = int(spaceCountDict[f"{nextLineSpace}_space_count"])
            currentSpaceCount = int(spaceCountDict[f"{currentLineSpace}_space_count"])

            # Check fir first element of strings list
            firstCondition = (
                currentLineSpace == 0 and nextLineSpace == 2 and nextSpaceCount > 1
            )
            secondCondition = (
                nextLineSpace == currentLineSpace
                or nextLineSpace > currentLineSpace
                or nextLineSpace == 0
            )

            if firstCondition:
                spaceCountDict[f"{currentLineSpace}_space_count"] = (
                    currentSpaceCount - 1
                )

                if spaceCountDict[f"{currentLineSpace}_space_count"] == 0:
                    treeDepthDict[f"depth_{currentDepth}"] = 0
                outputLine = lineInfo[0]

            elif secondCondition:
                spaceCountDict[f"{currentLineSpace}_space_count"] = (
                    currentSpaceCount - 1
                )

                # Calculating space multiplier
                if spaceCountDict[f"{currentLineSpace}_space_count"] == 0:
                    treeDepthDict[f"depth_{currentDepth}"] = 0
                spaceMiltiplier = self._increaseMultiplier(treeDepthDict)
                spaceMiltiplier = self._checkAndSetsetSpaceMultiplier(
                    spaceMiltiplier, currentDepth
                )

                # If last element with this depth set └─
                if spaceCountDict[f"{currentLineSpace}_space_count"] == 0:
                    outputLine = (
                        "    " * spaceMiltiplier
                        + ("│  " * ((currentDepth - spaceMiltiplier) - 1))
                        + "└─ "
                        + lineInfo[0]
                    )
                else:
                    outputLine = (
                        "    " * spaceMiltiplier
                        + ("│  " * ((currentDepth - spaceMiltiplier) - 1))
                        + "├─ "
                        + lineInfo[0]
                    )

            elif nextLineSpace < currentLineSpace:
                spaceCountDict[f"{currentLineSpace}_space_count"] = (
                    currentSpaceCount - 1
                )

                if spaceCountDict[f"{currentLineSpace}_space_count"] == 0:
                    treeDepthDict[f"depth_{currentDepth}"] = 0
                spaceMiltiplier = self._increaseMultiplier(treeDepthDict)
                spaceMiltiplier = self._checkAndSetsetSpaceMultiplier(
                    spaceMiltiplier, currentDepth
                )

                outputLine = (
                    "    " * spaceMiltiplier
                    + ("│  " * ((currentDepth - spaceMiltiplier) - 1))
                    + "└─ "
                    + lineInfo[0]
                )
            print(outputLine)
