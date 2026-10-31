from pathlib import Path

import pyray as rl


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120
PADDLE_SPEED = 460
BALL_RADIUS = 28
BALL_SPEED = 390


def main():
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Ping Pong")
    rl.set_target_fps(60)

    image_path = Path(__file__).with_name(
        "974eb514-85dd-4b32-9410-f27340093058.png"
    )
    ball_image = rl.load_image(str(image_path))
    if not rl.is_image_valid(ball_image):
        rl.close_window()
        raise FileNotFoundError(f"Could not load ball image: {image_path}")

    image_bounds = rl.get_image_alpha_border(ball_image, 0.01)
    cropped_ball_image = rl.image_from_image(ball_image, image_bounds)
    rl.unload_image(ball_image)
    ball_texture = rl.load_texture_from_image(cropped_ball_image)
    rl.unload_image(cropped_ball_image)

    background = rl.Color(19, 110, 125, 255)
    paddle_color = rl.Color(245, 220, 110, 255)
    left_paddle = rl.Rectangle(50, (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2,
                               PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = rl.Rectangle(SCREEN_WIDTH - 50 - PADDLE_WIDTH,
                                (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2,
                                PADDLE_WIDTH, PADDLE_HEIGHT)
    left_score = 0
    right_score = 0
    ball_x = SCREEN_WIDTH / 2
    ball_y = SCREEN_HEIGHT / 2
    ball_velocity_x = BALL_SPEED
    ball_velocity_y = BALL_SPEED * 0.45

    while not rl.window_should_close():
        frame_time = rl.get_frame_time()

        if rl.is_key_down(rl.KeyboardKey.KEY_W):
            left_paddle.y -= PADDLE_SPEED * frame_time
        if rl.is_key_down(rl.KeyboardKey.KEY_S):
            left_paddle.y += PADDLE_SPEED * frame_time
        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            right_paddle.y -= PADDLE_SPEED * frame_time
        if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
            right_paddle.y += PADDLE_SPEED * frame_time

        left_paddle.y = max(0, min(left_paddle.y, SCREEN_HEIGHT - PADDLE_HEIGHT))
        right_paddle.y = max(0, min(right_paddle.y, SCREEN_HEIGHT - PADDLE_HEIGHT))

        ball_x += ball_velocity_x * frame_time
        ball_y += ball_velocity_y * frame_time

        if ball_y - BALL_RADIUS <= 0:
            ball_y = BALL_RADIUS
            ball_velocity_y = abs(ball_velocity_y)
        elif ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
            ball_y = SCREEN_HEIGHT - BALL_RADIUS
            ball_velocity_y = -abs(ball_velocity_y)

        ball_center = rl.Vector2(ball_x, ball_y)
        if (ball_velocity_x < 0
                and rl.check_collision_circle_rec(ball_center, BALL_RADIUS, left_paddle)):
            ball_x = left_paddle.x + left_paddle.width + BALL_RADIUS
            hit_offset = (ball_y - (left_paddle.y + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2)
            ball_velocity_x = min(abs(ball_velocity_x) * 1.05, 700)
            ball_velocity_y = hit_offset * BALL_SPEED
        elif (ball_velocity_x > 0
              and rl.check_collision_circle_rec(ball_center, BALL_RADIUS, right_paddle)):
            ball_x = right_paddle.x - BALL_RADIUS
            hit_offset = (ball_y - (right_paddle.y + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2)
            ball_velocity_x = -min(abs(ball_velocity_x) * 1.05, 700)
            ball_velocity_y = hit_offset * BALL_SPEED

        if ball_x + BALL_RADIUS < 0:
            right_score += 1
            ball_x = SCREEN_WIDTH / 2
            ball_y = SCREEN_HEIGHT / 2
            ball_velocity_x = -BALL_SPEED
            ball_velocity_y = BALL_SPEED * 0.45
        elif ball_x - BALL_RADIUS > SCREEN_WIDTH:
            left_score += 1
            ball_x = SCREEN_WIDTH / 2
            ball_y = SCREEN_HEIGHT / 2
            ball_velocity_x = BALL_SPEED
            ball_velocity_y = BALL_SPEED * 0.45

        rl.begin_drawing()
        rl.clear_background(background)
        for y in range(0, SCREEN_HEIGHT, 32):
            rl.draw_rectangle(SCREEN_WIDTH // 2 - 2, y, 4, 16, rl.Color(210, 235, 230, 150))
        rl.draw_rectangle_rec(left_paddle, paddle_color)
        rl.draw_rectangle_rec(right_paddle, paddle_color)
        rl.draw_text(f"{left_score}     {right_score}", SCREEN_WIDTH // 2 - 85, 24, 40, rl.WHITE)
        rl.draw_text("W / S", 50, SCREEN_HEIGHT - 32, 18, rl.WHITE)
        rl.draw_text("UP / DOWN", SCREEN_WIDTH - 145, SCREEN_HEIGHT - 32, 18, rl.WHITE)

        source = rl.Rectangle(0, 0, ball_texture.width, ball_texture.height)
        destination = rl.Rectangle(
            ball_x - BALL_RADIUS,
            ball_y - BALL_RADIUS,
            BALL_RADIUS * 2,
            BALL_RADIUS * 2,
        )
        rl.draw_texture_pro(
            ball_texture, source, destination, rl.Vector2(0, 0), 0, rl.WHITE
        )
        rl.end_drawing()

    rl.unload_texture(ball_texture)
    rl.close_window()


if __name__ == "__main__":
    main()
