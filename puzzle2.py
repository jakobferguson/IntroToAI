import random
import copy
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

    #generates a random move
    #if the move is not valid then it will default to not moving
    #returns a value of which to move toad on the x axis of the last row
    def toad_move(self, choice):
        #choice = random.randint(1,5)
        if choice == 'A' and self.board[4].index('T')>=3:
            self.moves = self.moves + 'A'
            self.player_hp = self.player_hp - 2
            return -2
        elif choice == 'S' and self.board[4].index('T')>=2:
            self.moves = self.moves + 'S'
            self.player_hp = self.player_hp - 1
            return -1
        elif choice == 'F' and self.board[4].index('T')<=4:
            self.moves = self.moves + 'F'
            self.player_hp = self.player_hp - 1
            return 1
        elif choice == 'G' and self.board[4].index('T')<=3:
            self.moves = self.moves + 'G'
            self.player_hp = self.player_hp - 2
            return 2
        elif choice == 'D':
            self.moves = self.moves + 'D'
            self.player_hp = self.player_hp - 0
            return 0
        else:
            return None
    
    #returns true if alive, and false if not
    def next_turn(self, move):
        temp_game = copy.deepcopy(self)
        #print(temp_game.roll_queue)
        #move toad update health
        #returns false if its an invalid move
        new_move = temp_game.toad_move(move)
        if new_move is None:
            #print("Invalid move!")
            return False
        else:
            new_index = temp_game.board[4].index('T') + new_move
    
        temp_game.board[4][temp_game.board[4].index('T')] = ' '
        temp_game.board[4][new_index] = 'T'
        #move snakes down
        #   check if toad dead
        examined_row = temp_game.board.pop(3) #used to check fly and snake in next two game steps
        #add new row not actually used for calculations at this step so it is moved
        temp_game.board.insert(0, temp_game.potential_rolls[temp_game.roll_queue.pop(0)])
        snake_indexes = []
        for i in range(len(examined_row)):
            if examined_row[i] == 'S':
                snake_indexes.append(i)

        if new_index in snake_indexes:
            #toad died
            #print("Toad died to snakes!")
            return False
        #flies move down one
        #   see if toad eat fly
        if((new_index == 1 and examined_row[0] == 'F') or (new_index == 5 and examined_row[6] == 'F')):
            temp_game.player_hp+=5

        #add new row
        #print('turn ' + str(self.roll_queue[0]))
        #self.board.insert(0, self.potential_rolls[self.roll_queue.pop(0)])
        #print('new row added')
        #if toad health == 0 then end
        if temp_game.player_hp == 0:
            #print("Toad had no health!")
            return False
    
        return temp_game
    
    #shows end of game state
    def pretty_print(self, file_to_write_to):
        with open(file_to_write_to, 'w') as file:
            file.write(str(self.moves) + '\n')
            file.write(str(self.player_hp) + '\n')
            for i in range(5):
                for j in range(7):
                    file.write(str(self.board[i][j]))
                file.write("\n")
    '''
    def play(self):
        while(len(self.roll_queue) > 0):
            if not self.next_turn():
                return
            #self.pretty_print() used for debugging
    '''
            
    '''
    Expects an already created toad game object. Solves the game using bfs algorithm.

    :max_depth: how many turns deep the solver will attempt to go and return a solution for
    :available_actions: a list of what moves toad can make (A, S, D, F, G)
    :return: a solved board state in which toad wins if able
    '''
    def bfs_solver(self, max_turns, available_actions):
        frontier = []
        current_depth = 0

        '''
        q start board
        While frontier not empty and depth < max_depth
            current board = frontier[0]
            enqueue next state and all VALID actions
            remove current board from frontier
            depth++
        '''
        frontier.append(self)
        while frontier:
            #print("Current frontier on iteration " + str(current_depth))
            #print(frontier)
            current_depth+=1
            current_board = frontier.pop(0)
            #current_board.pretty_print()
            if len(current_board.moves) == max_turns:
                return current_board
            for move in available_actions: #append
                potential_board = current_board.next_turn(move)
                if potential_board:
                    frontier.append(potential_board)
            '''
            print("fimal frpmtier")
            for item in frontier:
                item.pretty_print()
            '''

        #return frontier[0] if frontier else None

def main():
    if __name__ == '__main__':

        rolls = []

        with open(sys.argv[1], 'r') as file:
            for i in range(int(file.readline().strip('\n'))):
                rolls.append(int(file.readline().strip('\n')))

        new_game = toad_game(rolls)

        solved_game = new_game.bfs_solver(num_turns, ['A', 'S', 'D', 'F', 'G'])
        #print("Solved")
        solved_game.pretty_print(sys.argv[2])

main()