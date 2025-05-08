import random
import sys

# class game creates instance of game
#need to track:
#game board, including whole state x
#player location x
#the queue of rolls for future turns
#game board updater
#   move old row
#   add new row
#   determine death or point
#toad move chooser
class toad_game:
    def __init__(self, roll_queue):
        '''
        BOARD KEY
        ' ' = empty space
        'S'  = snake location
        '#'  = bank
        'F'  = fly location
        'T'  = toad location
        '''
        self.board= [['#',' ',' ',' ',' ',' ','#'],
                     ['#',' ',' ',' ',' ',' ','#'],
                     ['#',' ',' ',' ',' ',' ','#'],
                     ['#',' ',' ',' ',' ',' ','#'],
                     ['#',' ',' ','T',' ',' ','#']]

        self.player_hp = 20
        self.moves = ''

        self.potential_rolls = [['#',' ',' ',' ',' ',' ','#'],
                                ['#',' ',' ',' ',' ','S','#'],
                                ['#',' ',' ',' ','S',' ','#'],
                                ['#',' ',' ',' ','S','S','#'],
                                ['#',' ',' ','S',' ',' ','#'],
                                ['#',' ',' ','S',' ','S','#'],
                                ['#',' ',' ','S','S',' ','#'],
                                ['#',' ',' ','S','S','S','#'],
                                ['#',' ','S',' ',' ',' ','#'],
                                ['#',' ','S',' ',' ','S','#'],
                                ['#',' ','S',' ','S',' ','#'],
                                ['#',' ','S',' ','S','S','#'],
                                ['#',' ','S','S',' ',' ','#'],
                                ['#',' ','S','S',' ','S','#'],
                                ['#',' ','S','S','S',' ','#'],
                                ['#',' ','S','S','S','S','#'],
                                ['#','S',' ',' ',' ',' ','#'],
                                ['#','S',' ',' ',' ','S','#'],
                                ['#','S',' ',' ','S',' ','#'],
                                ['#','S',' ',' ','S','S','#'],
                                ['#','S',' ','S',' ',' ','#'],
                                ['#','S',' ','S',' ','S','#'],
                                ['#','S',' ','S','S',' ','#'],
                                ['#','S',' ','S','S','S','#'],
                                ['#','S','S',' ',' ',' ','#'],
                                ['#','S','S',' ',' ','S','#'],
                                ['#','S','S',' ','S',' ','#'],
                                ['#','S','S',' ','S','S','#'],
                                ['#','S','S','S',' ',' ','#'],
                                ['#','S','S','S',' ','S','#'],
                                ['#','S','S','S','S',' ','#'],
                                ['#','S','S','S','S','S','#'],
                                ['F',' ',' ',' ',' ',' ','#'],
                                ['#',' ',' ',' ',' ',' ','F']]
        
        self.roll_queue = roll_queue

    #if the move is not valid then it will default to not moving
    def toad_move(self):
        choice = random.randint(1,5)
        if choice == 1 and self.board[4].index('T')>=3:
            self.moves = self.moves + 'A'
            self.player_hp = self.player_hp - 2
            return -2
        elif choice == 2 and self.board[4].index('T')>=2:
            self.moves = self.moves + 'S'
            self.player_hp = self.player_hp - 1
            return -1
        elif choice == 3 and self.board[4].index('T')<=4:
            self.moves = self.moves + 'F'
            self.player_hp = self.player_hp - 1
            return 1
        elif choice == 4 and self.board[4].index('T')<=3:
            self.moves = self.moves + 'G'
            self.player_hp = self.player_hp - 2
            return 2
        else:
            self.moves = self.moves + 'D'
            return 0
        
    #returns true if alive, and false if not
    def next_turn(self):
        #move toad update health
        new_index = self.board[4].index('T') + self.toad_move()
        self.board[4][self.board[4].index('T')] = ' '
        self.board[4][new_index] = 'T'
        #move snakes down
        #   check if toad dead
        examined_board = self.board.pop(3) #used to check fly and snake in next two game steps
        #add new row not actually used for calculations at this step so it is moved
        self.board.insert(0, self.potential_rolls[self.roll_queue.pop(0)])
        snake_indexes = []
        for i in range(len(examined_board)):
            if examined_board[i] == 'S':
                snake_indexes.append(i)

        if new_index in snake_indexes:
            #toad died
            return False
        #flies move down one
        #   see if toad eat fly
        if((new_index == 1 and examined_board[0] == 'F') or (new_index == 5 and examined_board[6] == 'F')):
            self.player_hp+=5

        #add new row
        #print('turn ' + str(self.roll_queue[0]))
        #self.board.insert(0, self.potential_rolls[self.roll_queue.pop(0)])
        #print('new row added')
        #if toad health == 0 then end
        if self.player_hp == 0:
            return False
    
        return True
    
    #shows end of game state
    def pretty_print(self, file_to_write_to):
        with open(file_to_write_to, 'w') as file:
            file.write(str(self.moves) + '\n')
            file.write(str(self.player_hp) + '\n')
            for i in range(5):
                for j in range(7):
                    file.write(str(self.board[i][j]))
                file.write("\n")

    def play(self):
        while(len(self.roll_queue) > 0):
            if not self.next_turn():
                return
            #self.pretty_print() used for debugging

def main():
    if __name__ == '__main__':

        rolls = []

        with open(sys.argv[1], 'r') as file:
            for i in range(int(file.readline().strip('\n'))):
                rolls.append(int(file.readline().strip('\n')))
        #print(rolls)
        new_game = toad_game(rolls)

        new_game.play()
        new_game.pretty_print(sys.argv[2])

main()