import tcod as libtcod

from entity import Entity
from inputHandlers import handle_keys
from map_objects.game_map import GameMap
from renderFunctions import clear_all, render_all


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    colors = {
        'dark_wall': libtcod.Color(0, 0, 0),
        'dark_ground': libtcod.Color(128,128,128)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.green)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [
        # npc,
        player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'Roguelike Jam', False)

    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, entities, game_map, screen_width, screen_height, colors)
        libtcod.console_set_default_foreground(0, libtcod.green)
        libtcod.console_put_char(0, player.x, player.y, '@', libtcod.BKGND_NONE)
        libtcod.console_flush()

        clear_all(con, entities)
        libtcod.console_put_char(0, player.x, player.y, ' ', libtcod.BKGND_NONE)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
     main()