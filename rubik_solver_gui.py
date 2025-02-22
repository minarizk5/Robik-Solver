from ssl import SSLSocket
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                           QHBoxLayout, QWidget, QGridLayout, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import kociemba

class CubeFace(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.colors = {
            'U': QColor(255, 255, 255),  # White
            'R': QColor(255, 0, 0),      # Red
            'F': QColor(0, 255, 0),      # Green
            'D': QColor(255, 255, 0),    # Yellow
            'L': QColor(255, 165, 0),    # Orange
            'B': QColor(0, 0, 255)       # Blue
        }
        self.current_color = self.colors[color]
        self.setFixedSize(40, 40)
        self.setAutoFillBackground(True)
        self.update_color()

    def update_color(self):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.current_color)
        self.setPalette(palette)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            colors = list(self.colors.keys())
            current_index = colors.index(self.get_color_letter())
            next_index = (current_index + 1) % len(colors)
            self.current_color = self.colors[colors[next_index]]
            self.update_color()

    def get_color_letter(self):
        for letter, color in self.colors.items():
            if color == self.current_color:
                return letter
        return 'U'  # Default to white if not found

class RubiksCubeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rubik's Cube Solver")      
        self.setFixedSize(800, 600)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Create cube display
        cube_widget = QWidget()
        cube_layout = QHBoxLayout(cube_widget)
        
        # Create faces layout
        self.faces = {}
        face_layouts = {}
        face_widgets = {}
        
        # Define face positions and their default colors
        face_positions = {
            'U': (0, 1), 'L': (1, 0), 'F': (1, 1),
            'R': (1, 2), 'B': (1, 3), 'D': (2, 1)
        }
        
        # Create grid for all faces
        faces_grid = QGridLayout()
        faces_grid.setSpacing(10)
        
        # Create each face
        for face, pos in face_positions.items():
            face_widgets[face] = QWidget()
            face_layouts[face] = QGridLayout(face_widgets[face])
            self.faces[face] = []
            
            # Create 3x3 grid for each face
            for i in range(3):
                row = []
                for j in range(3):
                    square = CubeFace(face)
                    face_layouts[face].addWidget(square, i, j)
                    row.append(square)
                self.faces[face].append(row)
            
            faces_grid.addWidget(face_widgets[face], pos[0], pos[1])

        # Add faces grid to main layout
        main_layout.addLayout(faces_grid)

        # Add buttons
        button_layout = QHBoxLayout()
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self.solve_cube)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_cube)
        button_layout.addWidget(solve_button)
        button_layout.addWidget(reset_button)
        main_layout.addLayout(button_layout)

        # Add solution display
        self.solution_label = QLabel("Solution will appear here")
        self.solution_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.solution_label)

        # Add instructions
        instructions = QLabel(
            "Instructions:\n"
            "1. Click on squares to change colors\n"
            "2. Set up the cube state as you see it\n"
            "3. Click 'Solve' to get the solution"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)

    def get_cube_state(self):
        state = ''
        # Order: U, R, F, D, L, B
        faces_order = ['U', 'R', 'F', 'D', 'L', 'B']
        for face in faces_order:
            for row in self.faces[face]:
                for square in row:
                    state += square.get_color_letter()
        return state

    def solve_cube(self):
        try:
            cube_state = self.get_cube_state()
            solution = kociemba.solve(cube_state)
            formatted_solution = self.format_solution(solution)
            self.solution_label.setText(formatted_solution)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid cube state: {str(e)}")

    def format_solution(self, solution):
        moves = solution.split()
        return ' → '.join(moves)

    def reset_cube(self):
        for face in self.faces.values():
            for row in face:
                for square in row:
                    square.current_color = square.colors[square.color]
                    square.update_color()
        self.solution_label.setText("Solution will appear here")

def main():
    app = QApplication(sys.argv)
    window = RubiksCubeGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
