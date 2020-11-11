import time
import tkinter as tk
from tkinter import *
from calculate_routes import calculate_route

super_matrix = [
    ["0", 'C', "Oranges", "Apples", "Pears", "Watermelons", "Melons", "Strawberries", "Blackberries", 'W'],
    ["Potatoes", 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', "Tomatoes"],
    ["Onions", 'C', 'W', 'W', 'W', 'W', 'W', 'W', 'C', "Cucumbers"],
    ["Honey", 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', "Peppers"],
    ['W', "Bamba", 'C', "Pesek Zman", 'W', "Salt", 'C', 'C', 'C', "Garlics"],
    ['W', "Bisli", 'C', "Baunti", 'W', "Sugar", 'C', 'W', 'W', 'W'],
    ['W', "Doritos", 'C', "Popcorn", 'W', "Tea", 'C', "Frozen corn", "Frozen chips", "Ice cream"],
    ['W', "Chips", 'C', "Red Bamba", 'W', "Coffee", 'C', 'C', 'C', 'C'],
    ["Bread", 'C', 'C', 'C', 'C', 'C', 'C', "Eggs", "Hummus", "Salads"],
    ['W', "Milk", 'C', "White cheese", 'W', "Butter", 'C', 'W', 'W', 'W']]
super_matrix2 = [
    ["0", 'C', "Oranges", "Apples", "Pears", "Watermelons", "Melons", "Strawberries", "Blackberries", 'Blueberries'],
    ["Potatoes", 'C', 'C', 'C', 'C', 'W', 'C', 'C', 'C', "Tomatoes"],
    ["Onions", 'C', 'W', 'W', 'W', 'W', 'W', 'W', 'C', "Cucumbers"],
    ["Lemons", 'C', 'C', 'C', 'C', 'W', 'Honey', 'C', 'C', "Peppers"],
    ['W', "Bamba", 'C', "W", 'W', "Salt", 'W', 'C', 'C', "Garlics"],
    ['W', "Bisli", 'C', "Baunti", 'C', "Sugar", 'C', 'W', 'W', 'W'],
    ['W', "Doritos", 'C', "Popcorn", 'C', "Tea", 'C', "Frozen corn", "Frozen chips", "Ice cream"],
    ['W', "Chips", 'C', "Red Bamba", 'C', "Coffee", 'C', 'C', 'C', 'C'],
    ["Bread", 'C', 'C', 'C', 'C', 'C', 'C', "Eggs", "Hummus", "Salads"],
    ['W', "Milk", 'C', "White cheese", 'W', "Butter", 'C', 'W', 'W', 'W']]

super_matrix3 = [
    ["0", 'C', "Oranges", "Apples", "Pears", "Watermelons", "Melons", "Strawberries", "Blackberries", 'Blueberries'],
    ["Potatoes", 'C', 'C', 'C', 'C', 'W', 'C', 'C', 'C', "Tomatoes"],
    ["Onions", 'C', 'W', 'W', 'W', 'W', 'W', 'W', 'C', "Cucumbers"],
    ["Lemons", 'C', 'C', 'C', 'C', 'no!', 'Honey', 'C', 'C', "Peppers"],
    ['W', "Bamba", 'C', "W", 'W', "Salt", 'W', 'C', 'C', "Garlics"],
    ['W', "Bisli", 'C', "Baunti", 'C', "Sugar", 'C', 'W', 'W', 'W'],
    ['W', "Doritos", 'C', "Popcorn", 'C', "Tea", 'C', "Frozen corn", "Frozen chips", "Ice cream"],
    ['W', "Chips", 'C', "Red Bamba", 'C', "Coffee", 'C', 'C', 'C', 'C'],
    ["Bread", 'C', 'C', 'C', 'C', 'C', 'C', "Eggs", "Hummus", "Salads"],
    ['W', "Milk", 'C', "White cheese", 'W', "Butter", 'C', 'W', 'W', 'W']]
super_matrixes = {'Super 1': super_matrix, 'Super 2': super_matrix2, 'Super 3':super_matrix3}


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.left = InputFrame(self, master=self.master)
        self.right = SuperView(self, master=self.master)
        self.left.pack(side="left", expand=False, fill="both")
        self.right.pack(side="right", expand=True, fill="both")

    def change_matrix(self, selected_option):
        self.right.paint_grid(super_matrixes[selected_option])

    def paint_it(self, matrix):
        self.right.paint_grid(matrix)


class InputFrame(tk.Frame):
    def __init__(self, application, master=None):
        super().__init__(master, borderwidth=2, relief="solid")
        self.application = application
        self.master = master
        self.choices = {}
        self.choices = self.select_option_from_superDLL()
        self.load_select_product_frame()
        self.selected_matrix_name = 'Super 1'
        self.selected_product_label = Label(master=self, text="No product was selected")

    def get_selected_matrix_name(self):
        return self.selected_matrix_name

    def load_select_product_frame(self):
        def next_button_pressed():
            try:
                listbox.insert(END, v.get())
                E1.delete(0, END)
            except:
                return

        def send_button_pressed():
            # values [listbox.get(index) for index in range(0,END) listbox.get(0,END)]
            values = list(listbox.get(0, END))
            listbox.delete(0, END)

            route, products_coors = calculate_route(super_matrixes[self.selected_matrix_name], values)
            editted_matrix = self.prepare_matrix_for_new_painting(super_matrixes[self.selected_matrix_name], [],
                                                                  products_coors)
            self.application.paint_it(editted_matrix)
            dynamic_route_painting(editted_matrix, route, 4, products_coors)
            editted_matrix = self.prepare_matrix_for_new_painting(super_matrixes[self.selected_matrix_name], route,
                                                                  products_coors)
            self.application.paint_it(editted_matrix)

        def dynamic_route_painting(matrix, route, snake_len, products_coors):
            self.application.paint_it(matrix)
            route = route + [(0, 0)] * (snake_len - 1)
            for j in range(3):
                for i, coor in enumerate(route):

                    tail = route[i - snake_len - 1]
                    if i - snake_len >= 0: matrix[tail[0]][tail[1]] = str(matrix[tail[0]][tail[1]])  if tail in products_coors else 'C'

                    snake = route[i - snake_len:i]
                    for snake_coor in snake:
                        if not snake_coor in products_coors:
                            matrix[snake_coor[0]][snake_coor[1]] = 'R'
                    self.application.paint_it(matrix)
                    self.master.update()
                    time.sleep(0.1)

        frame = Frame(master=self)
        frame.pack(side="bottom", expand=False)
        v = StringVar()
        E1 = Entry(frame, bd=5, textvariable=v)
        E1.pack(side='right')
        L1 = Label(frame, text="Product Name:")
        L1.pack(side='top')
        next_product_button = Button(master=self, text="Type Next Product", width=20, command=next_button_pressed)
        next_product_button.pack()
        send_button = Button(master=self, text="Calculate Route", width=20, command=send_button_pressed)
        send_button.pack()
        listbox = Listbox(master=self)
        listbox.pack()

    def select_option_from_superDLL(self):
        # Add a grid
        mainframe = Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.pack(pady=100, padx=100)

        # Create a Tkinter variable
        tkvar = StringVar(self)

        # Dictionary with options
        choices = super_matrixes.keys()
        self.choices = choices
        tkvar.set('Super 1')  # set the default option
        popupMenu = OptionMenu(mainframe, tkvar, *choices)
        Label(mainframe, text="Choose a supermarket").grid(row=1, column=1)
        popupMenu.grid(row=2, column=1)

        def change_dropdown(*args):
            self.change_matrix(tkvar.get())

        tkvar.trace('w', change_dropdown)
        return choices

    def change_matrix(self, selected_option):
        self.selected_matrix_name = selected_option
        self.application.change_matrix(selected_option)

    def prepare_matrix_for_new_painting(self, matrix, route, products_coors):
        copy_matrix = [row[:] for row in matrix]
        for i, row in enumerate(matrix):
            for j, item in enumerate(row):
                if (i, j) in products_coors:
                    copy_matrix[i][j] = 'Selected ' + str(matrix[i][j])
                elif (i, j) in route:
                    copy_matrix[i][j] = 'R'
        return copy_matrix


class SuperView(tk.Frame):
    def __init__(self, application, master=None):
        super().__init__(master, borderwidth=2, relief="solid")
        self.application = application
        self.master = master
        self.grid = self.paint_grid(super_matrix)  # Paint it according to the first matrix

    def paint_grid(self, matrix):
        for widget in self.winfo_children():
            widget.destroy()
        Grid.rowconfigure(super(), 0, weight=1)
        Grid.columnconfigure(super(), 0, weight=1)
        frame = Frame(self, borderwidth=2, relief="solid")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.clipboard_clear()
        for row_index in range(len(matrix)):
            Grid.rowconfigure(self, row_index, weight=1)
            for col_index in range(len(matrix[0])):
                Grid.columnconfigure(self, col_index, weight=1)
                btn = Button(self, bg=paint_style(matrix, row_index, col_index),
                             text=self.write_product_by_super(matrix, row_index, col_index),
                             fg="black")  # create a button inside frame
                # if super_matrix[row_index][col_index]
                btn.grid(row=row_index, column=col_index, sticky="nsew")
        return frame.grid

    def write_product_by_super(self, matrix, row_index, col_index):
        if matrix[row_index][col_index] == 'W' or matrix[row_index][col_index] == 'C' or matrix[row_index][
            col_index] == '0' or matrix[row_index][col_index] == 'R':
            return ""
        else:
            return matrix[row_index][col_index]


def paint_style(matrix, row, col):
    if matrix[row][col] == 'C':
        return "white"
    if matrix[row][col] == 'W':
        return "black"
    if matrix[row][col] == 'R':
        return "green"
    if matrix[row][col].startswith('Selected'):
        return "yellow"
    if matrix[row][col] == '0':
        return "white"
    return "blue"  # products


def main():
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.title("Superpy")
    root.geometry("800x600")
    # root.resizable(0, 0)
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
