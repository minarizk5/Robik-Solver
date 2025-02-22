import kociemba

def validate_cube_state(cube_string):
    """
    Validate if the cube state string is valid (54 characters, proper colors)
    """
    if len(cube_string) != 54:
        return False
    
    # Valid colors in Rubik's cube
    valid_colors = {'U', 'R', 'F', 'D', 'L', 'B'}
    
    # Check if all characters are valid colors
    for char in cube_string:
        if char not in valid_colors:
            return False
    
    # Check if each face has exactly 9 pieces
    color_count = {}
    for char in cube_string:
        color_count[char] = color_count.get(char, 0) + 1
    
    for count in color_count.values():
        if count != 9:
            return False
            
    return True

def get_cube_state():
    """
    Get the current state of the Rubik's Cube from user input
    Standard notation: U (up), R (right), F (front), D (down), L (left), B (back)
    """
    print("\nEnter the cube state in the following order:")
    print("U1-U9 (Up face), R1-R9 (Right face), F1-F9 (Front face),")
    print("D1-D9 (Down face), L1-L9 (Left face), B1-B9 (Back face)")
    print("Use: U for White, R for Red, F for Green, D for Yellow, L for Orange, B for Blue")
    
    cube_state = input("\nEnter the cube state (54 characters): ").strip().upper()
    
    while not validate_cube_state(cube_state):
        print("\nInvalid cube state! Please enter a valid cube state.")
        print("Make sure:")
        print("- String is exactly 54 characters long")
        print("- Uses only valid colors (U, R, F, D, L, B)")
        print("- Each color appears exactly 9 times")
        cube_state = input("\nEnter the cube state (54 characters): ").strip().upper()
    
    return cube_state

def solve_cube(cube_state):
    """
    Solve the Rubik's Cube using Kociemba's algorithm
    """
    try:
        # Solve the cube
        solution = kociemba.solve(cube_state)
        return solution
    except Exception as e:
        return f"Error solving cube: {str(e)}"

def format_solution(solution):
    """
    Format the solution moves to be more readable
    """
    moves = solution.split()
    formatted_moves = []
    
    for i, move in enumerate(moves, 1):
        formatted_moves.append(f"{i}. {move}")
    
    return "\n".join(formatted_moves)

def main():
    print("Welcome to Rubik's Cube Solver!")
    print("=================================")
    
    while True:
        # Get cube state
        cube_state = get_cube_state()
        
        print("\nSolving cube...")
        # Solve the cube
        solution = solve_cube(cube_state)
        
        if solution.startswith("Error"):
            print(solution)
        else:
            print("\nSolution found!")
            print("\nFollow these moves to solve the cube:")
            print("=====================================")
            print(format_solution(solution))
            print("\nMove notation:")
            print("U, R, F, D, L, B: Clockwise turns")
            print("U', R', F', D', L', B': Counter-clockwise turns")
            print("U2, R2, F2, D2, L2, B2: Double turns")
        
        # Ask if user wants to solve another cube
        choice = input("\nWould you like to solve another cube? (y/n): ").lower()
        if choice != 'y':
            print("\nThank you for using Rubik's Cube Solver!")
            break

if __name__ == "__main__":
    main()