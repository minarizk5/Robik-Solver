import tkinter as tk
from tkinter import ttk, messagebox
import kociemba

class CubeSquare(tk.Canvas):
    def __init__(self, parent, color, size=40):
        super().__init__(parent, width=size, height=size, highlightthickness=1, highlightbackground="black")
        self.size = size
        self.colors = {
            'U': "white",
            'R': "red",
            'F': "green",
            'D': "yellow",
            'L': "orange",
            'B': "blue"
        }
        self.color_list = list(self.colors.keys())
        self.current_color = self.colors[color]
        self.draw_square()
        self.bind("<Button-1>", self.change_color)

    def draw_square(self):
        self.delete("all")
        self.create_rectangle(2, 2, self.size-2, self.size-2, fill=self.current_color, outline="black")

    def change_color(self, event):
        current_letter = self.get_color_letter()
        current_index = self.color_list.index(current_letter)
        next_index = (current_index + 1) % len(self.color_list)
        self.current_color = self.colors[self.color_list[next_index]]
        self.draw_square()

    def get_color_letter(self):
        for letter, color in self.colors.items():
            if color == self.current_color:
                return letter
        return 'U'

class RubiksCubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube Solver")
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create cube faces
        self.faces = {}
        face_positions = {
            'U': (0, 1), 'L': (1, 0), 'F': (1, 1),
            'R': (1, 2), 'B': (1, 3), 'D': (2, 1)
        }

        # Create frames for each face
        for face, pos in face_positions.items():
            face_frame = ttk.Frame(main_frame)
            face_frame.grid(row=pos[0], column=pos[1], padx=5, pady=5)
            
            self.faces[face] = []
            for i in range(3):
                row = []
                for j in range(3):
                    square = CubeSquare(face_frame, face)
                    square.grid(row=i, column=j)
                    row.append(square)
                self.faces[face].append(row)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        solve_button = ttk.Button(button_frame, text="Solve", command=self.solve_cube)
        solve_button.grid(row=0, column=0, padx=5)

        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_cube)
        reset_button.grid(row=0, column=1, padx=5)

        # Solution display
        self.solution_var = tk.StringVar(value="Solution will appear here")
        solution_label = ttk.Label(main_frame, textvariable=self.solution_var, wraplength=400)
        solution_label.grid(row=4, column=0, columnspan=4, pady=10)

        # Instructions
        instructions = """Instructions:
1. Click on squares to change colors
2. Set up the cube state as you see it
3. Click 'Solve' to get the solution"""
        instruction_label = ttk.Label(main_frame, text=instructions, justify=tk.LEFT)
        instruction_label.grid(row=5, column=0, columnspan=4, pady=10)

    def get_cube_state(self):
        state = ''
        faces_order = ['U', 'R', 'F', 'D', 'L', 'B']
        for face in faces_order:
            for row in self.faces[face]:
                for square in row:
                    state += square.get_color_letter()
        return state

    def solve_cube(self):
        try:
            cube_state = self.get_cube_state()
            
            # Import validation function from Robik Solver module
            import importlib.util
            spec = importlib.util.spec_from_file_location("robik_solver", "Robik Solver.py")
            robik_solver = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(robik_solver)
            
            # Validate the cube state first
            if not robik_solver.validate_cube_state(cube_state):
                messagebox.showerror("Error", "Invalid cube state! Please ensure:\n- Each color appears exactly 9 times\n- Colors are properly distributed")
                return
                
            solution = kociemba.solve(cube_state)
            formatted_solution = ' → '.join(solution.split())
            self.solution_var.set(formatted_solution)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid cube state: {str(e)}")

    def reset_cube(self):
        for face, squares in self.faces.items():
            for row in squares:
                for square in row:
                    square.current_color = square.colors[face]
                    square.draw_square()
        self.solution_var.set("Solution will appear here")

def main():
    root = tk.Tk()
    app = RubiksCubeGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
