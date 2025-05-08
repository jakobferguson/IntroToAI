import copy
import heapq
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
            return None
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
            return None
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
            return None
    
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

    def goal(self, moves):
        #print(moves)
        #making this a function also allows for potential extra goals to be added later

        #functionally is a transition function as well, because of next_turn being an all in one this is necessary without complete refactoring
        solved = copy.deepcopy(self)
        for move in list(moves):
            solved = solved.next_turn(move)
            if solved == None:
                return None
        #print(str(len(moves)),str(len(self.roll_queue)))
        if len(moves) == len(self.roll_queue):    
            return solved #only win condition atm is surviving all the rounds
        else:
            return None
            
    '''
    :return: a solved board state in which toad wins if able
    '''
    #a frontier was getting too confusing and taking a while, so i swapped to using a recursive function to try and minimize computation time
    def a_star_solver(self, available_actions):
        open_list = []
        heapq.heappush(open_list, GameStateWrapper(self, 0)) #awesome library!
        visited = set()

        while open_list:
            current_wrapper = heapq.heappop(open_list)
            current_state = current_wrapper.state

            if len(current_state.roll_queue) == 0:
                return current_state
            
            state_signature = (tuple(map(tuple, current_state.board)), current_state.player_hp, current_state.moves) #keeps track of states without a whole class instance
            if state_signature in visited:
                continue
            visited.add(state_signature)

            for move in available_actions:
                next_state = current_state.next_turn(move)
                if next_state:
                    heapq.heappush(open_list, GameStateWrapper(next_state, len(next_state.moves)))
        return None

class GameStateWrapper:
            def __init__(self, state, cost):
                self.state = state
                self.cost = cost
                self.heuristic = len(state.roll_queue)
                self.priority = self.cost + self.heuristic

            def __lt__(self, other):
                return self.priority < other.priority

def main():
    if __name__ == '__main__':

        rolls = []

        with open(sys.argv[1], 'r') as file:
            num_turns = int(file.readline().strip('\n'))
            for i in range(num_turns):
                rolls.append(int(file.readline().strip('\n')))

        new_game = toad_game(rolls)

        solved_game = new_game.a_star_solver(['A', 'S', 'D', 'F', 'G'])
        #print("Solved")
        solved_game.pretty_print(sys.argv[2])

main()