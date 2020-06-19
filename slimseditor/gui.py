import sys

import bimpy
import filedialog


def main():
    ctx = bimpy.Context()
    ctx.init(600, 600, "Slim's Editor")

    str = bimpy.String()
    f = bimpy.Float();

    file_open_clicked = bimpy.Bool()
    file_quit_clicked = bimpy.Bool()

    test_window_opened = bimpy.Bool()

    while(not ctx.should_close()):
        with ctx:
            #bimpy.new_frame()
            if bimpy.begin_main_menu_bar():
                if bimpy.begin_menu('File'):
                    bimpy.menu_item('Open', 'Cmd+F', file_open_clicked)
                    if file_open_clicked.value:
                        print(filedialog.open_file())

                    bimpy.menu_item('Quit', 'Cmd+Q', file_quit_clicked)
                    if file_quit_clicked.value:
                        return


            bimpy.begin('Test Window', test_window_opened)
            bimpy.end()


if __name__ == "__main__":
    main()
