import curses
import random


def game_loop(window):
    # Setup inicial
    curses.curs_set(0)
    snake = [
        [10, 15],
        [9, 15],
    ]
    fruit = get_new_fruit(window=window)
    current_direction = curses.KEY_DOWN
    snake_ate_fruit = False

    while True:
        draw_screen(window=window)
        draw_snake(snake=snake, window=window)
        draw_actor(actor=fruit, window=window, char=curses.ACS_DIAMOND)

        direction = get_new_direction(window=window, timeout=1000)

        if direction is None:
            direction = current_direction

        move_snake(snake=snake, direction=direction, snake_ate_fruit=snake_ate_fruit)

        if snake_hit_border(snake=snake, window=window):
            return

        if snake_hit_fruit(snake=snake, fruit=fruit):
            snake_ate_fruit = True
            fruit = get_new_fruit(window=window)
        else:
            snake_ate_fruit = False

        current_direction = direction


def get_new_fruit(window):
    height, width = window.getmaxyx()
    return [random.randint(1, height - 2), random.randint(1, width - 2)]


def snake_hit_border(snake, window):
    head = snake[0]
    return actor_hit_border(actor=head, window=window)


def snake_hit_fruit(snake, fruit):
    return fruit in snake


def draw_screen(window):
    window.clear()
    window.border(0)


def draw_snake(snake, window):
    head = snake[0]
    draw_actor(actor=head, window=window, char="♛")
    body = snake[1:]
    for body_part in body:
        draw_actor(actor=body_part, window=window, char="✱")


def draw_actor(actor, window, char):
    window.addch(actor[0], actor[1], char)


def get_new_direction(window, timeout):
    window.timeout(timeout)
    direction = window.getch()
    if direction in [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_RIGHT]:
        return direction
    return None


def move_snake(snake, direction, snake_ate_fruit):
    head = snake[0].copy()
    move_actor(actor=head, direction=direction)
    snake.insert(0, head)

    if not snake_ate_fruit:
        snake.pop()


def move_actor(actor, direction):
    match direction:
        case curses.KEY_UP:
            actor[0] -= 1
        case curses.KEY_LEFT:
            actor[1] -= 1
        case curses.KEY_DOWN:
            actor[0] += 1
        case curses.KEY_RIGHT:
            actor[1] += 1


def actor_hit_border(actor, window):
    height, width = window.getmaxyx()
    if (actor[0] <= 0) or (actor[0] >= height - 1):
        return True
    if (actor[1] <= 0) or (actor[1] >= width - 1):
        return True
    return False


if __name__ == "__main__":
    curses.wrapper(game_loop)
    print("-------------------------")
    print("Você perdeu!!")
    print("-------------------------")
