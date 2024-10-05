import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListView, QHBoxLayout, QCheckBox, QStyledItemDelegate
from PySide6.QtCore import QStringListModel, Qt

class TaskDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        task = index.data(Qt.DisplayRole)
        if "✔" in task:
            option.font.setStrikeOut(True)
        super().paint(painter, option, index)

class TodoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List App")
        self.setGeometry(100, 100, 400, 300)

        self.tasks = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.task_list = QListView()
        self.task_list.setEditTriggers(QListView.NoEditTriggers)
        self.task_list.setSelectionMode(QListView.SingleSelection)
        self.task_list.setItemDelegate(TaskDelegate())
        self.layout.addWidget(self.task_list)
        self.label = QLabel("Enter a task:")
        self.layout.addWidget(self.label)

        self.task_input = QLineEdit()
        self.layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_task)
        self.layout.addWidget(self.remove_button)

        self.mark_completed_button = QPushButton("Mark as Completed")
        self.mark_completed_button.clicked.connect(self.mark_task_completed)
        self.layout.addWidget(self.mark_completed_button)

        self.update_task_list()

    def add_task(self):
        task = self.task_input.text()
        if task:
            self.tasks.append((task, False))
            self.task_input.clear()
            self.update_task_list()

    def remove_task(self):
        selected_index = self.task_list.currentIndex()
        if selected_index.isValid():
            del self.tasks[selected_index.row()]
            self.update_task_list()

    def mark_task_completed(self):
        selected_index = self.task_list.currentIndex()
        if selected_index.isValid():
            task, completed = self.tasks[selected_index.row()]
            self.tasks[selected_index.row()] = (task, not completed)
            self.update_task_list()

    def update_task_list(self):
        formatted_tasks = [f"✔ {task}" if completed else task for task, completed in self.tasks]
        self.task_list.setModel(QStringListModel(formatted_tasks))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoListApp()
    window.show()
    sys.exit(app.exec())
