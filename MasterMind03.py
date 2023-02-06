import random

#Tu código va aquí
class MasterMindGame:
    #declaramos las variables que vamos a utilizar
    
    MMC = {} #diccionario de colores válidos.   

    secretCode = [] #código secreto que tenemos que adivinar.

    validColors = "rgybkw" #colores mastermind permitidos    
    
    maxTurns = 10 #máximo número de turnos para acertar la clave.
    currentTurn = 0 #turno actual.
    wonGame = False

    mmTopPlayers = {}

    playerName = ""
    
    
    #construimos la función para iniciar la clase
    def __init__(self,name = "noName",
     combiCode:str = "nocombiCode"):
        #iniciamos el diccionario de colores
        if combiCode == "nocombiCode":
            self.secretCode = MasterMindGame.randomCode(self, 4)
        else:
            try:
                self.secretCode = MasterMindGame.toMasterMindColorCombination(self,combiCode)
            except:
                self.secretCode = MasterMindGame.randomCode(self, 4)
        self.playerName = name
        self.readTopPlayers()
            
        self.MMC["red"] = "🔴"
        self.MMC["green"] = "🟢"
        self.MMC["yellow"] = "🟡"
        self.MMC["blue"] = "🔵"
        self.MMC["black"] = "⚫"
        self.MMC["white"] = "⚪"

    def readTopPlayers(self):
        try:
            f = open("topMMPlayers.txt", "r")
            a = f.read()
            split  = a.split("#")
            for x in split:
                if x != "":
                    player = x.split("-")
                    self.mmTopPlayers[player[0]] = int(player[1])
            print(self.mmTopPlayers)
            f.close()
        except:
            print("No se ha podido leer el archivo topplayers.txt")
    
    def updateTopPlayers(self, name:str, turns:int):
        # if this turn is less than the top 3 of the dictionary replace it
        bandera = False
        if name in self.mmTopPlayers:
            if turns < self.mmTopPlayers[name]:
                self.mmTopPlayers[name] = turns
                print( "estas dentro de los 3 mejores jugadores")
                print("Se ha actualizado el puntaje de " + name + " a " + str(turns) + " turnos")
                self.printTopPlayers()
                bandera = True
        else:
            if len(self.mmTopPlayers) < 3:
                self.mmTopPlayers[name] = turns
                bandera = True
            else:
                for x in self.mmTopPlayers:
                    if turns < self.mmTopPlayers[x]:
                        self.mmTopPlayers[name] = turns
                        print( "estas dentro de los 3 mejores jugadores")
                        del self.mmTopPlayers[x]
                        self.printTopPlayers()
                        bandera = True
                        break
        return bandera

    def printTopPlayers(self):
        print("Los mejores jugadores son:")
        for x in self.mmTopPlayers:
            print("MVP "+x + " acertó la clave en " + str(self.mmTopPlayers[x]) + " intentos") 
    
    def writeTopPlayers(self):
        try:
            f = open("topMMPlayers.txt", "w")
            for x in self.mmTopPlayers:
                f.write(x + "-" + str(self.mmTopPlayers[x]) + "#")
            f.close()
        except:
            print("No se ha podido escribir el archivo topplayers.txt")


        
    def randomCode(self, k:int):#genera un código aleatorio
        return random.choices(self.validColors, k=k)
                
    def MasterMindColor(self, color:str): #convertir cadenas en colores
        rcolor = "Color no encontrado"

        MMC = {}

        MMC["red"] = "🔴"
        MMC["green"] = "🟢"
        MMC["yellow"] = "🟡"
        MMC["blue"] = "🔵"
        MMC["black"] = "⚫"
        MMC["white"] = "⚪"

        if color.upper() == 'R' or color == '🔴':
            return MMC["red"]
        elif color.upper() == 'G' or color == '🟢':
            return MMC["green"]
        elif color.upper() == 'Y' or color == '🟡':
            return MMC["yellow"]
        elif color.upper() == 'B' or color == '🔵':
            return MMC["blue"]
        elif color.upper() == 'K' or color == '⚫':
            return  MMC["black"]
        elif color.upper() == 'W' or color == '⚪':
            return MMC["white"]
        else:
            return MMC[rcolor]

    def toMasterMindColorCombination (self, combi:str): #obtener una cadena de colores mastermind
        return list(map(lambda n: MasterMindGame.MasterMindColor(self,n), combi))
        
    #Recibe un array de colores MasterMind y devuelve los aciertos comparando con secretcode
    def countExactMatches(self, mmcombi: list) -> int:
        cmatches = 0
        
        for v in range(0, len(mmcombi)):
            if mmcombi[v] == self.MasterMindColor(self.secretCode[v]):
                cmatches += 1
        
        return cmatches

    #Recibe un array de colores MasterMInd y devuelve los semiaciertos comparando con secretcode
    def countPartialMatches(self, mmcombi: list) -> int:
        smatches = 0
        secretCodeFails = []
        mmcombiFails = []
        
        for n in range(0, len(mmcombi)):
            if mmcombi[n] != self.MasterMindColor(self.secretCode[n]):
                mmcombiFails.append(mmcombi[n])
                secretCodeFails.append(self.MasterMindColor(self.secretCode[n]))

        for x in secretCodeFails:
            if x in mmcombiFails:
                smatches += 1

        return smatches
    
    def newTurn(self, guess:str):
        testCombination = []
        
        try:
            testCombination = self.toMasterMindColorCombination(guess)
        except:
            print("Combinación incorrecta. Por favor, prueba de nuevo")
            return
            
        try:
            if len(self.secretCode) != len(testCombination):
                raise NameError('HiThere')
        except:
            print("Debes hacer una apuesta con ",len(self.secretCode)," colores. Por favor, prueba de nuevo.")
            return;
            
        try:
            if self.currentTurn == self.maxTurns:
                raise NameError('HiThere')
        except:
            print("El juego ha terminado.")
            return
            
        if self.wonGame == False:
            self.currentTurn += 1
            print("Turno: %s." % self.currentTurn)
            print("Tu combinación: %s" % testCombination)
            totalMatches = MasterMindGame.countExactMatches(self, testCombination)
            semiMatches = MasterMindGame.countPartialMatches(self, testCombination)
            
            if totalMatches == len(self.secretCode):
                print("Has ganado en el turno %s!" % self.currentTurn)
                self.wonGame = True
                updated = self.updateTopPlayers(self.playerName, self.currentTurn)
                if updated:
                    self.writeTopPlayers()
                return
            elif self.currentTurn == self.maxTurns:
                print("Lo siento, has perdido. Otra vez será.")
                return
            
            print("Aciertos: %s" % totalMatches)
            print("Semiaciertos: %s" % semiMatches)
        else:
            print("El juego ha terminado.")
def main():
    name = input("Introduce tu nombre: ")
    game = MasterMindGame(name)
    while game.wonGame == False:
        
        guess = input("Introduce una combinación de colores: ")
        game.newTurn(guess)

if __name__ == "__main__":
    main()


