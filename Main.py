# - School Comments
#! Nebin Comments
#Todo Added Changes
#? Possible Questions
# - _: Protected __:Private +:Public


import random

def Main():
    SimulationParameters = [] #! Setting empty simulation parameters.
    SimNo = input("Enter simulation number: ")

    #TODO Simulation Number validation

    if int(SimNo) < 0 or int(SimNo) > 5:
        print("Invalid simulation number, try again")
        Main()
        
    if SimNo == "1":
        SimulationParameters = [1, 5, 5, 500, 3, 5, 1000, 50]
    elif SimNo == "2":
        SimulationParameters = [1, 5, 5, 500, 3, 5, 1000, 100]
    elif SimNo == "3":
        SimulationParameters = [1, 10, 10, 500, 3, 9, 1000, 25]
    elif SimNo == "4":
        SimulationParameters = [2, 10, 10, 500, 3, 6, 1000, 25]
    ThisSimulation = Simulation(SimulationParameters) #!Instantiation
    Choice = "" #! Setting empty choice
    while Choice != "9": #! As long as we do not exit the program we...
        DisplayMenu()
        Choice = GetChoice()
        if Choice == "1":
            print(ThisSimulation.GetDetails()) #! Method referring to the details of the simulation
        elif Choice == "2": #!Displaying the details of the area
            StartRow = 0
            StartColumn = 0
            EndRow = 0
            EndColumn = 0
            StartRow, StartColumn = GetCellReference()
            EndRow, EndColumn = GetCellReference()
            print(ThisSimulation.GetAreaDetails(StartRow, StartColumn, EndRow, EndColumn))
        elif Choice == "3": #!Displaying the information of a cell
            Row = 0
            Column = 0
            Row, Column = GetCellReference()
            print(ThisSimulation.GetCellDetails(Row, Column))
        elif Choice == "4": #!Advancing one stage.
            ThisSimulation.AdvanceStage(1)
            print("Simulation moved on one stage\n")
        elif Choice == "5": #!Advancing more than one stage.
            NumberOfStages = int(input("Enter number of stages to advance by: "))
            ThisSimulation.AdvanceStage(NumberOfStages)
            print(f"Simulation moved on {NumberOfStages} stages" + "\n")
        elif Choice == "6":
            ThisSimulation.PrintSummary() 
        elif Choice == "7":
            ThisSimulation.PrintAnts()
        elif Choice == "8":
            ThisSimulation.PrintDeliver()
        elif Choice == "9":
            quit()
    input()

def DisplayMenu(): #!Function which is called in Main() where it prints the main menu ?Possible question adds onto the menu?
    print()
    print("1. Display overall details")
    print("2. Display area details")
    print("3. Inspect cell")
    print("4. Advance one stage")
    print("5. Advance X stages")
    print("6. Display Summary")
    print("7. Display Ants")
    print("8. Print Ant Food Delivery")
    print("9. Quit")
    print()
    print("> ", end='')

def GetChoice():
    Choice = input() #!Input
    return Choice 

#TODO CellReference validation
def GetCellReference(Sim):
    print()
    Hold = False
    while Hold == False:
        Row = int(input("Enter row number: "))
        if Row>=1 and Row<=Sim._NumberOfRows:
            Hold = True
        else:
            print("Invalid row number, try again")
            Hold = False
            
    Hold = False
    while Hold == False:
        Col = int(input("Enter column number: "))
        if Col>=1 and Col<=Sim._NumberOfColumns:
            Hold = True
        else:
            print("Invalid column number, try again")
            Hold = False

class Simulation():
    def __init__(self, SimulationParameters): #!{Protected data}, accessible by using the array. We can create another simulation from this.
        self._StartingNumberOfNests = SimulationParameters[0]
        self._NumberOfRows = SimulationParameters[1]
        self._NumberOfColumns = SimulationParameters[2]
        self._StartingFoodInNest = SimulationParameters[3]
        self._StartingNumberOfFoodCells = SimulationParameters[4]
        self._StartingAntsInNest = SimulationParameters[5]
        self._NewPheromoneStrength = SimulationParameters[6]
        self._PheromoneDecay = SimulationParameters[7]
        self._Nests = [] #Next 4 will be filled with objects
        self._Ants = []
        self._Pheromones = []
        self._Grid = []
        self._AntList = {}
        self._FoodDelivery = dict[int,int]()

        Row = 0
        Column = 0
        for Row in range(1, self._NumberOfRows + 1):
            for Column in range(1, self._NumberOfColumns + 1):
                self._Grid.append(Cell(Row, Column))
        self.SetUpANestAt(2, 4)
        for Count in range(2, self._StartingNumberOfNests + 1):
            Allowed = False
            while Allowed == False:
                Allowed = True
                Row = random.randint(1, self._NumberOfRows) #!Randomly setting the Row and Column number for the nest meaning they are always randomly generated.
                Column = random.randint(1, self._NumberOfColumns)
                for N in self._Nests:
                    if N.GetRow() == Row and N.GetColumn() == Column: #!Checking that an nest is not already in use.
                        Allowed = False
            self.SetUpANestAt(Row, Column) #!Creating the nest
        for Count in range(1, self._StartingNumberOfFoodCells + 1):
            Allowed = False
            while Allowed == False:
                Allowed = True
                Row = random.randint(1, self._NumberOfRows)
                Column = random.randint(1, self._NumberOfColumns)
                for N in self._Nests:
                    if N.GetRow() == Row and N.GetColumn() == Column:
                        Allowed = False
            self.AddFoodToCell(Row, Column,500) #!Is not checking that there is not a food cell already there but will check that if there is a nest there.

    def PrintSummary(self):
        print("===Simulation Summary===\n")
        print(f"Grid Size {self._NumberOfColumns},{self._NumberOfRows}\n")
        print(f"Number of nests is {len(self._Nests)}\n")
        print(f"Number of ants is {len(self._Ants)}\n")
        food = 0 

        for c in self._Grid:
            food += c.GetAmountOfFood()
        print(f"Total food {food}")

    def PrintAnts(self):
        print("List of all ants")
        for ant in self._Ants:
            print(f"ID {ant._ID}, Type is {ant._TypeOfAnt}, Nest is at {ant._NestRow}, {ant._NestColumn}")

    def PrintDeliver(self):
        print("Ant Food Delivered")
        print("==================")
        totalFood = 0
        for AntID, Qty in self._FoodDelivery.items():
            print(AntID, " ", Qty)
            totalFood += Qty
        print("Total food delivered is ", totalFood)
        return

    def SetUpANestAt(self, Row, Column): #!Setting up the nest
        self._Nests.append(Nest(Row, Column, self._StartingFoodInNest)) 
        self._Ants.append(QueenAnt(Row, Column, Row, Column)) #Adds the queen ant
        for Worker in range(2, self._StartingAntsInNest + 1):
            self._Ants.append(WorkerAnt(Row, Column, Row, Column)) #Adds the worker ant

    def AddFoodToCell(self, Row, Column, Quantity): #!Adding food indicates that the food cell which add onto food that might already be there.
        self._Grid[self.__GetIndex(Row, Column)].UpdateFoodInCell(Quantity)

    def __GetIndex(self, Row, Column):
        return (Row - 1) * self._NumberOfColumns + Column - 1

    def __GetIndicesOfNeighbours(self, Row, Column): #!Returns the index numbers of the neighbouring cells
        ListOfNeighbours = []
        for RowDirection in [-1, 0, 1]:
            for ColumnDirection in [-1, 0, 1]:
                NeighbourRow = Row + RowDirection
                NeighbourColumn = Column + ColumnDirection
                if (RowDirection != 0 or ColumnDirection != 0) and NeighbourRow >= 1 and NeighbourRow <= self._NumberOfRows and NeighbourColumn >= 1 and NeighbourColumn <= self._NumberOfColumns:
                    ListOfNeighbours.append(self.__GetIndex(NeighbourRow, NeighbourColumn))
                else:
                    ListOfNeighbours.append(-1)
        return ListOfNeighbours

    def __GetIndexOfNeighbourWithStrongestPheromone(self, Row, Column):
        StrongestPheromone = 0
        IndexOfStrongestPheromone = -1
        for Index in self.__GetIndicesOfNeighbours(Row, Column):
            if Index != -1 and self.GetStrongestPheromoneInCell(self._Grid[Index]) > StrongestPheromone:
                IndexOfStrongestPheromone = Index
                StrongestPheromone = self.GetStrongestPheromoneInCell(self._Grid[Index])
        return IndexOfStrongestPheromone

    def GetNestInCell(self, C):
        for N in self._Nests:
            if N.InSameLocation(C):
                return N
        return None

    def UpdateAntsPheromoneInCell(self, A):
        for P in self._Pheromones:
            if P.InSameLocation(A) and P.GetBelongsTo() == A.GetID():
                P.UpdateStrength(self._NewPheromoneStrength)
                return
        self._Pheromones.append(Pheromone(A.GetRow(), A.GetColumn(), A.GetID(), self._NewPheromoneStrength, self._PheromoneDecay))

    def GetNumberOfAntsInCell(self, C):
        Count = 0
        for A in self._Ants:
            if A.InSameLocation(C):
                Count += 1
        return Count

    def GetNumberOfPheromonesInCell(self, C):
        Count = 0
        for P in self._Pheromones:
            if P.InSameLocation(C):
                Count += 1
        return Count

    def GetStrongestPheromoneInCell(self, C):
        Strongest = 0
        for P in self._Pheromones:
            if P.InSameLocation(C):
                if P.GetStrength() > Strongest:
                    Strongest = P.GetStrength()
        return Strongest

    def GetDetails(self):
        Details = ""
        for Row in range(1, self._NumberOfRows + 1):
            for Column in range(1, self._NumberOfColumns + 1):
                Details += f"{Row}, {Column}: "
                TempCell = self._Grid[self.__GetIndex(Row, Column)]
                if self.GetNestInCell(TempCell) is not None:
                    Details += "| Nest |  "
                NumberOfAnts = self.GetNumberOfAntsInCell(TempCell)
                if NumberOfAnts > 0:
                    Details += f"| Ants: {NumberOfAnts} |  "
                NumberOfPheromones = self.GetNumberOfPheromonesInCell(TempCell)
                if NumberOfPheromones > 0:
                    Details += f"| Pheromones: {NumberOfPheromones} |  "
                AmountOfFood = TempCell.GetAmountOfFood()
                if AmountOfFood > 0:
                    Details += f"| {AmountOfFood} food |  "
                Details += "\n"
        return Details

    def GetAreaDetails(self, StartRow, StartColumn, EndRow, EndColumn):
        Details = ""
        for Row in range(StartRow, EndRow + 1):
            for Column in range(StartColumn, EndColumn + 1):
                Details += f"{Row}, {Column}: "
                TempCell = self._Grid[self.__GetIndex(Row, Column)]
                if self.GetNestInCell(TempCell) is not None:
                    Details += "| Nest |  "
                NumberOfAnts = self.GetNumberOfAntsInCell(TempCell)
                if NumberOfAnts > 0:
                    Details += f"| Ants: {NumberOfAnts} |  "
                NumberOfPheromones = self.GetNumberOfPheromonesInCell(TempCell)
                if NumberOfPheromones > 0:
                    Details += f"| Pheromones: {NumberOfPheromones} |  "
                AmountOfFood = TempCell.GetAmountOfFood()
                if AmountOfFood > 0:
                    Details += f"| {AmountOfFood} food |  "
                Details += "\n"
        return Details

    def AddFoodToNest(self, Food, Row, Column):
        for N in self._Nests:
            if N.GetRow() == Row and N.GetColumn() == Column:
                N.ChangeFood(Food)
                return

    def GetCellDetails(self, Row, Column):
        CurrentCell = self._Grid[self.__GetIndex(Row, Column)]
        Details = CurrentCell.GetDetails()
        N = self.GetNestInCell(CurrentCell)
        if N is not None:
            Details += f"Nest present ({N.GetFoodLevel()} food)" + "\n\n"
        if self.GetNumberOfAntsInCell(CurrentCell) > 0:
            Details += "ANTS\n"
            for A in self._Ants:
                if A.InSameLocation(CurrentCell):
                    Details += A.GetDetails() + "\n"
            Details += "\n\n"
        if self.GetNumberOfPheromonesInCell(CurrentCell) > 0:
            Details += "PHEROMONES\n"
            for P in self._Pheromones:
                if P.InSameLocation(CurrentCell):
                    Details += f"Ant {P.GetBelongsTo()} with strength of {P.GetStrength()}" + "\n\n"
            Details += "\n\n"
        return Details

    def AdvanceStage(self, NumberOfStages):
        for Count in range(1, NumberOfStages + 1):
            PheromonesToDelete = []
            for P in self._Pheromones:
                P.AdvanceStage(self._Nests, self._Ants, self._Pheromones)
                if P.GetStrength() == 0:
                    PheromonesToDelete.append(P)
            for P in PheromonesToDelete:
                self._Pheromones.remove(P)
            for A in self._Ants:
                A.AdvanceStage(self._Nests, self._Ants, self._Pheromones)
                CurrentCell = self._Grid[self.__GetIndex(A.GetRow(), A.GetColumn())]
                if A.GetFoodCarried() > 0 and A.IsAtOwnNest():
                    qty = A.GetFoodCarried()
                    self.AddFoodToNest(qty, A.GetRow(), A.GetColumn())
                    # Record delivery per-ant
                    self._FoodDelivery.setdefault(A.GetID(), 0)
                    self._FoodDelivery[A.GetID()] += qty
                    A.UpdateFoodCarried(-qty)
                elif CurrentCell.GetAmountOfFood() > 0 and A.GetFoodCarried() == 0 and A.GetFoodCapacity() > 0:
                    FoodObtained = CurrentCell.GetAmountOfFood() + 1
                    while FoodObtained > CurrentCell.GetAmountOfFood() or (A.GetFoodCarried() + FoodObtained) > A.GetFoodCapacity():
                        FoodObtained = random.randint(1, A.GetFoodCapacity())
                    CurrentCell.UpdateFoodInCell(-FoodObtained)
                    A.UpdateFoodCarried(FoodObtained)
                else:
                    if A.GetFoodCarried() > 0:
                        self.UpdateAntsPheromoneInCell(A)
                    A.ChooseCellToMoveTo(self.__GetIndicesOfNeighbours(A.GetRow(), A.GetColumn()), self.__GetIndexOfNeighbourWithStrongestPheromone(A.GetRow(), A.GetColumn()))
            for N in self._Nests:
                self._Nests, self._Ants, self._Pheromones = N.AdvanceStage(self._Nests, self._Ants, self._Pheromones)

class Entity():
    def __init__(self, StartRow, StartColumn):
        self._Row = StartRow
        self._Column = StartColumn
        self._ID = None

    def InSameLocation(self, E):
        return E.GetRow() == self._Row and E.GetColumn() == self._Column

    def GetRow(self):
        return self._Row

    def GetColumn(self):
        return self._Column

    def GetID(self):
        return self._ID

    def AdvanceStage(self, Nests, Ants, Pheromones):
        pass

    def GetDetails(self):
        return "" #? Possible question to return some other values possible in a f string.

class Cell(Entity):
    def __init__(self, StartRow, StartColumn):
        super().__init__(StartRow, StartColumn)
        self._AmountOfFood = 0

    def GetAmountOfFood(self):
        return self._AmountOfFood

    def GetDetails(self):
        Details = f"{super().GetDetails()}{self._AmountOfFood} food present" + "\n\n"
        return Details

    def UpdateFoodInCell(self, Change):
        self._AmountOfFood += Change

class Ant(Entity):
    _NextAntID = 1

    def __init__(self, StartRow, StartColumn, NestInRow, NestInColumn):
        super().__init__(StartRow, StartColumn)
        self._NestRow = NestInRow
        self._NestColumn = NestInColumn
        self._ID = Ant._NextAntID
        Ant._NextAntID += 1
        self._Stages = 0
        self._AmountOfFoodCarried = 0
        self._FoodCapacity = 0
        self._TypeOfAnt = ""

    def GetFoodCapacity(self):
        return self._FoodCapacity

    def IsAtOwnNest(self):
        return self._Row == self._NestRow and self._Column == self._NestColumn

    def AdvanceStage(self, Nests, Ants, Pheromones):
        self._Stages += 1
        return

    def GetDetails(self):
        return f"{super().GetDetails()}  Ant {self._ID}, {self._TypeOfAnt}, stages alive: {self._Stages}"

    def UpdateFoodCarried(self, Change):
        self._AmountOfFoodCarried += Change

    def _ChangeCell(self, NewCellIndicator, RowToChange, ColumnToChange):
        if NewCellIndicator > 5:
            RowToChange += 1
        elif NewCellIndicator < 3:
            RowToChange -= 1
        if NewCellIndicator in [0, 3, 6]:
            ColumnToChange -= 1
        elif NewCellIndicator in [2, 5, 8]:
            ColumnToChange += 1
        return RowToChange, ColumnToChange

    def _ChooseRandomNeighbour(self, ListOfNeighbours):
        Chosen = False
        while Chosen == False:
            RNo = random.randint(0, len(ListOfNeighbours) - 1)
            if ListOfNeighbours[RNo] != -1:
                Chosen = True
        return RNo

    def ChooseCellToMoveTo(self, ListOfNeighbours, IndexOfNeighbourWithStrongestPheromone):
        pass

    def GetFoodCarried(self):
        return self._AmountOfFoodCarried

    def GetNestRow(self):
        return self._NestRow

    def GetNestColumn(self):
        return self._NestColumn

    def GetTypeOfAnt(self):
        return self._TypeOfAnt

class QueenAnt(Ant):
    def __init__(self, StartRow, StartColumn, NestInRow, NestInColumn):
        super().__init__(StartRow, StartColumn, NestInRow, NestInColumn)
        self._TypeOfAnt = "queen"

class WorkerAnt(Ant):
    def __init__(self, StartRow, StartColumn, NestInRow, NestInColumn):
        super().__init__(StartRow, StartColumn, NestInRow, NestInColumn)
        self._TypeOfAnt = "worker"
        self._FoodCapacity = 30

    def GetDetails(self):
        return f"{super().GetDetails()}, carrying {self._AmountOfFoodCarried} food, home nest is at {self._NestRow} {self._NestColumn}"

    def ChooseCellToMoveTo(self, ListOfNeighbours, IndexOfNeighbourWithStrongestPheromone):
        if self._AmountOfFoodCarried > 0:
            if self._Row > self._NestRow:
                self._Row -= 1
            elif self._Row < self._NestRow:
                self._Row += 1
            if self._Column > self._NestColumn:
                self._Column -= 1
            elif self._Column < self._NestColumn:
                self._Column += 1
        elif IndexOfNeighbourWithStrongestPheromone == -1:
            IndexToUse = self._ChooseRandomNeighbour(ListOfNeighbours)
            self._Row, self._Column = self._ChangeCell(IndexToUse, self._Row, self._Column)
        else:
            IndexToUse = ListOfNeighbours.index(IndexOfNeighbourWithStrongestPheromone)
            self._Row, self._Column = self._ChangeCell(IndexToUse, self._Row, self._Column)

class Nest(Entity):
    _NextNestID = 1

    def __init__(self, StartRow, StartColumn, StartFood):
        super().__init__(StartRow, StartColumn)
        self._FoodLevel = StartFood
        self._NumberOfQueens = 1
        self._ID = Nest._NextNestID
        Nest._NextNestID += 1

    def ChangeFood(self, Change):
        self._FoodLevel += Change
        if self._FoodLevel < 0:
            self._FoodLevel = 0

    def GetFoodLevel(self):
        return self._FoodLevel

    def AdvanceStage(self, Nests, Ants, Pheromones):
        if Ants is None:
            return
        AntsToCull = 0
        Count = 0
        AntsInNestCount = 0
        for A in Ants:
            if A.GetNestRow() == self._Row and A.GetNestColumn() == self._Column:
                if A.GetTypeOfAnt() == "queen":
                    Count += 10
                else:
                    Count += 2
                    AntsInNestCount += 1
        self.ChangeFood(-int(Count))
        if self._FoodLevel == 0 and AntsInNestCount > 0:
            AntsToCull += 1
        if self._FoodLevel < AntsInNestCount:
            AntsToCull += 1
        if self._FoodLevel < AntsInNestCount * 5:
            AntsToCull += 1
            if AntsToCull > AntsInNestCount:
                AntsToCull = AntsInNestCount
            for A in range(1, AntsToCull + 1):
                RPos = random.randint(0, len(Ants) - 1)
                while not(Ants[RPos].GetNestRow() == self._Row and Ants[RPos].GetNestColumn() == self._Column):
                    RPos = random.randint(0, len(Ants) - 1)
                if Ants[RPos].GetTypeOfAnt() == "queen":
                    self._NumberOfQueens -= 1
                Ants.pop(RPos)
        else:
            for A in range(1, self._NumberOfQueens + 1):
                RNo1 = random.randint(0, 99)
                if RNo1 < 50:
                    RNo2 = random.randint(0, 99)
                    if RNo2 < 2:
                        Ants.append(QueenAnt(self._Row, self._Column, self._Row, self._Column))
                        self._NumberOfQueens += 1
                    else:
                        Ants.append(WorkerAnt(self._Row, self._Column, self._Row, self._Column))
        return Nests, Ants, Pheromones

class Pheromone(Entity):
    def __init__(self, Row, Column, BelongsToAnt, InitialStrength, Decay):
        super().__init__(Row, Column)
        self._BelongsTo = BelongsToAnt
        self._Strength = InitialStrength
        self._PheromoneDecay = Decay

    def AdvanceStage(self, Nests, Ants, Pheromones):
        self._Strength -= self._PheromoneDecay
        if self._Strength < 0:
            self._Strength = 0

    def UpdateStrength(self, Change):
        self._Strength += Change

    def GetStrength(self):
        return self._Strength

    def GetBelongsTo(self):
        return self._BelongsTo

if __name__ == "__main__":
    Main()
