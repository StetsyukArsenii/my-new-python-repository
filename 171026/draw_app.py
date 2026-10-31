import pyray as rl


def find_image_frame(img: rl.Image) -> rl.Rectangle:
    up_left.x, up_left.y = 0, 0
    width, height = 0,0
    for y in range(img.height):
        for x in range(img.width):
            pixel_color = rl.get_image_color(img, x, y)
    return rl.Rectangle(up_left.x, up_left.y, width, height)

            

def main():
    rl.set_config_flags(rl.ConfigFlags.FLAG_WINDOW_RESIZABLE)
    rl.init_window(800, 600, "Draw App")

    lines = []
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        
        for line in lines:
            rl.draw_line_ex(line[0], line[1], 3, rl.BLACK)

        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            mouse_pos = rl.get_mouse_position()
            lines.append((prev_mouse_pos, mouse_pos))
        

        if rl.is_key_down(rl.KeyboardKey.KEY_O):
            if lines:
                lines.pop()
        if rl.is_key_down(rl.KeyboardKey.KEY_SPACE):
            img = rl.load_image_from_screen()
            rl.export_image(img, "drawing.png")
            rl.unload_image(img)
        if rl.is_key_down(rl.KeyboardKey.KEY_R):
            img = rl.load_image_from_sreen()
            frame = find_image_frame(img)
            rl.draw_rectangle_lines_ex(frame, 2, rl.RED)
            rl.export_image(img, "drawing.png")


        prev_mouse_pos = rl.get_mouse_position()
        rl.end_drawing()
    rl.close_window()



if __name__ == "__main__":
    main()