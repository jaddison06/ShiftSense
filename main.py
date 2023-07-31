import tkinter as tk
from tkinter import ttk
from typing import TypeVar, Callable, Optional

SHIFT_T = tuple[str, str, int]

T = TypeVar('T')
def listView(frame: tk.Frame, title: str, getInput: Callable[[tk.Frame, Callable[[T], None]], tk.Widget], toString: Callable[[T], str], initialList: Optional[list[T]] = None):
    ttk.Label(frame, text=title).pack()
    frames: list[tk.Frame] = []
    items: list[T] = initialList if initialList is not None else []
    def update():
        for currentFrame in frames:
            currentFrame.destroy()
            del currentFrame
        for i, item in enumerate(items):
            currentFrame = tk.Frame(frame)
            ttk.Label(currentFrame, text=toString(item)).pack(side=tk.LEFT)
            ttk.Button(currentFrame, text='Remove', command=lambda i=i: deleteItemCB(i)).pack(side=tk.RIGHT)
            currentFrame.pack()
            frames.append(currentFrame)

    def newItemCB(item: T):
        items.append(item)
        update()
    def deleteItemCB(idx: int):
        print(items)
        print(f'Deleting #{idx}')
        del items[idx]
        update()
    getInput(frame, newItemCB).pack()

def clear(*inputs: ttk.Entry):
    for input in inputs:
        input.delete(0, len(input.get()))

def newCB(root: tk.Tk):
    win = tk.Toplevel(root)

    staffList: list[str] = []
    shiftList: list[SHIFT_T] = []

    def staffInput(frame: tk.Frame, newItemCB: Callable[[str], None]) -> tk.Widget:
        inputFrame = tk.Frame(frame)
        entry = ttk.Entry(inputFrame)
        def addCB():
            newItemCB(entry.get())
            clear(entry)
        add = ttk.Button(inputFrame, text='Add', command=addCB)
        entry.pack(side=tk.LEFT)
        add.pack(side=tk.RIGHT)
        return inputFrame

    def shiftInput(frame: tk.Frame, newItemCB: Callable[[SHIFT_T], None]) -> tk.Widget:
        inputFrame = tk.Frame(frame)
        startInput = ttk.Entry(inputFrame)
        finishInput = ttk.Entry(inputFrame)
        lengthInput = ttk.Entry(inputFrame)
        def addCB():
            start = startInput.get()
            finish = finishInput.get()
            length = lengthInput.get()
            try:
                int(length)
            except ValueError:
                return
            newItemCB((start, finish, int(length)))
            clear(startInput, finishInput, lengthInput)

        add = ttk.Button(inputFrame, text='Add', command=addCB)
        startInput.pack(side=tk.LEFT)
        finishInput.pack(side=tk.LEFT)
        lengthInput.pack(side=tk.LEFT)
        add.pack(side=tk.RIGHT)

        return inputFrame

    staff = tk.Frame(win)
    shifts = tk.Frame(win)

    listView(staff, 'Staff', staffInput, lambda name: name)
    listView(shifts, 'Shifts', shiftInput, lambda shift: f'{shift[0]}-{shift[1]}')

    staff.pack(side=tk.LEFT)
    shifts.pack(side=tk.RIGHT)


def openCB(root: tk.Tk):
    win = tk.Toplevel(root)
    ttk.Label(win, text='balls').pack()


def main():
    win = tk.Tk()
    win.geometry('500x350')
    win.title('ShiftSense')

    center = ttk.Frame()

    new = ttk.Button(center, text='New Rota', command=lambda: newCB(win))
    open = ttk.Button(center, text='Open Rota', command=lambda: openCB(win))

    new.pack()
    open.pack()

    center.place(relx=.5, rely=.5, anchor=tk.CENTER)

    win.mainloop()


if __name__ == '__main__': main()
