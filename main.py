from gui_classes import MasterWindow, conn

try:
    root = MasterWindow()
    root.mainloop()
except Exception as e:
    print(e)
else:
    conn.commit()
finally:
    conn.close()

