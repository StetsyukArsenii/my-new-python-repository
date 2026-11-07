from pathlib import Path

import pyray as rl


def find_image_frame(img: rl.Image) -> rl.Rectangle:
    min_x, min_y = img.width, img.height
    max_x, max_y = -1, -1
    background = rl.RAYWHITE

    for y in range(img.height):
        for x in range(img.width):
            pixel = rl.get_image_color(img, x, y)
            if (pixel.r, pixel.g, pixel.b) != background[:3]:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if max_x == -1:
        return rl.Rectangle(0, 0, 0, 0)

    return rl.Rectangle(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)


def main():
    rl.set_config_flags(rl.ConfigFlags.FLAG_WINDOW_RESIZABLE)
    rl.init_window(600, 400, "Drawd App")

    lines = list()
    prev_mousePos = rl.vector2_zero()
    thick = 3
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        for line in lines:
            rl.draw_line_ex(line[0], line[1], thick, (0,0,0,255))
        rl.end_drawing()

        
        if rl.is_mouse_button_down(rl.MouseButton.MOUSE_BUTTON_LEFT):
            lines.append((prev_mousePos, rl.get_mouse_position()))
        prev_mousePos = rl.get_mouse_position()

        
        if (rl.is_key_down(rl.KeyboardKey.KEY_LEFT_CONTROL) and
            rl.is_key_down(rl.KeyboardKey.KEY_Z)):
            if len(lines):
                lines.pop()
        if rl.is_key_pressed(rl.KeyboardKey.KEY_C):
            lines.clear()
        if rl.is_key_released(rl.KeyboardKey.KEY_SPACE):
            img = rl.load_image_from_screen()
            frame = find_image_frame(img)

            if frame.width > 0 and frame.height > 0:
                rl.image_crop(img, frame)

            output_path = Path(__file__).resolve().parent / "hand-written-digit.jpg"
            

            rl.unload_image(img)

    rl.close_window()


if __name__ == '__main__':
    main()