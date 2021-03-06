#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import rect, text, actions, director
from cocos.sprite import Sprite
from pyglet.resource import ResourceNotFoundException, image as pyglet_image

from ...utils.constants import Colors
from ....utils.constants import C

__author__ = 'fyabc'

_Width, _Height = None, None


def get_width():
    global _Width, _Height
    if _Width is None:
        _Width, _Height = director.director.get_window_size()
    return _Width


def get_height():
    global _Width, _Height
    if _Height is None:
        _Width, _Height = director.director.get_window_size()
    return _Height


def pos(x, y, base=None, scale=1.0):
    if base is not None:
        return base[0] * x * scale, base[1] * y * scale
    global _Width, _Height
    if _Width is None:
        _Width, _Height = director.director.get_window_size()
    return _Width * x * scale, _Height * y * scale


def pos_x(x, base=None, scale=1.0):
    return pos(x, 0.0, base, scale)[0]


def pos_y(y, base=None, scale=1.0):
    return pos(0.0, y, base, scale)[1]


def get_label_box(label: text.Label):
    """Get the box of the label.

    :return: A rect that contains the label.
    """
    x, y = label.x, label.y
    width, height = label.element.content_width, label.element.content_height

    if label.element.anchor_x == 'left':
        pass
    elif label.element.anchor_x == 'center':
        x -= width / 2
    elif label.element.anchor_x == 'right':
        x -= width
    else:
        raise ValueError('Invalid x anchor: {}'.format(label.element.anchor_x))

    # Note: may need to fix 'center' and 'baseline' for multi-line label?
    if label.element.anchor_y == 'top':
        y -= height
    elif label.element.anchor_y == 'center':
        y -= height / 2
    elif label.element.anchor_y == 'baseline':
        pass
    elif label.element.anchor_y == 'bottom':
        pass
    else:
        raise ValueError('Invalid x anchor: {}'.format(label.element.anchor_x))

    world_x, world_y = label.parent.point_to_world((x, y))
    world_r, world_t = label.parent.point_to_world((x + width, y + height))

    return rect.Rect(world_x, world_y, world_r - world_x, world_t - world_y)


def get_sprite_box(sprite: Sprite):
    aabb = sprite.get_AABB()
    global_bl = sprite.parent.point_to_world(aabb.bottomleft)
    global_tr = sprite.parent.point_to_world(aabb.topright)
    return rect.Rect(*global_bl, *(global_tr - global_bl))


def alpha_color(color, alpha):
    return tuple(color[:3]) + (alpha,)


def try_load_image(name, image_part=None, image_size=None, default=None):
    """

    :param name: Image name.
    :param image_part: 4-element tuple of image part: (x, y, width, height), values in range [0.0, 1.0].
    :param image_size: 2-element tuple of image size: (width, height). If not given, get it from image data.
    :param default: Backup image name.
    :return: The loaded image, None if resource not found.
    """
    try:
        image = pyglet_image(name)
    except ResourceNotFoundException:
        if default is not None:
            image = pyglet_image(default)
        else:
            image = None
    if image is None:
        return None
    if image_part is not None:
        if image_size is None:
            image_size = image.width, image.height
        image = image.get_region(
            x=int(image_part[0] * image_size[0]), y=int(image_part[1] * image_size[1]),
            width=int(image_part[2] * image_size[0]), height=int(image_part[3] * image_size[1]))
    return image


def try_remove(self, child):
    """Remove a child from a CocosNode safely."""
    if isinstance(child, str):
        if child in self.children_names:
            self.remove(child)
    else:
        if child in self:
            self.remove(child)


def try_add(self, child, name=None, z=0):
    """Add a child to a CocosNode safely."""
    if name is None:
        if child not in self:
            self.add(child, z=z)
    else:
        if name not in self.children_names:
            self.add(child, name=name, z=z)


def set_menu_style(self, **kwargs):
    # you can override the font that will be used for the title and the items
    # you can also override the font size and the colors. see menu.py for
    # more info

    title_size = kwargs.pop('title_size', 64)
    item_size = kwargs.pop('item_size', 32)
    selected_size = kwargs.pop('selected_size', item_size)

    default_font = C.UI.Cocos.Fonts.Default.Name

    self.font_title['font_name'] = kwargs.pop('font_name', default_font)
    self.font_title['font_size'] = title_size
    self.font_title['color'] = Colors['whitesmoke']

    self.font_item['font_name'] = kwargs.pop('font_name', default_font)
    self.font_item['color'] = Colors['white']
    self.font_item['font_size'] = item_size
    self.font_item_selected['font_name'] = kwargs.pop('font_name', default_font)
    self.font_item_selected['color'] = Colors['green1']
    self.font_item_selected['font_size'] = selected_size


DefaultLabelStyle = {
    'font_name': C.UI.Cocos.Fonts.Default.Name,
    'font_size': 28,
    'anchor_x': 'center',
    'anchor_y': 'baseline',
    'color': Colors['whitesmoke'],
}


def hs_style_label(text_='', position=(0, 0), **kwargs):
    kw_with_default = DefaultLabelStyle.copy()
    kw_with_default.update(kwargs)
    return text.Label(text_, position, **kw_with_default)


class NoticeLabel(text.Label):
    """A notice label with default HearthStone style.

    This label will fade out after `time` seconds, then will be automatically removed from its parent.
    """

    def __init__(self, *args, **kwargs):
        time = kwargs.pop('time', 1.5)
        action_container = kwargs.pop('action_container', self)

        super().__init__(*args, **kwargs)

        action_container.do(actions.FadeOut(time) + actions.CallFunc(self.remove_self), target=self)

    def remove_self(self):
        self.parent.remove(self)


def notice(layer_, text_, **kwargs):
    """Add a notice label with default HearthStone style."""

    kw_with_default = DefaultLabelStyle.copy()
    kw_with_default.update({
        'time': 1.5, 'position': pos(0.5, 0.5),
        'anchor_y': 'center', 'font_size': 32,
        'color': Colors['yellow'],
    })

    kw_with_default.update(kwargs)
    layer_.add(NoticeLabel(text_, **kw_with_default))


def popup_input(title, width=250, height=70):
    import tkinter
    import tkinter.ttk as ttk

    master = tkinter.Tk()
    master.title(title)

    scr_width, scr_height = master.winfo_screenwidth(), master.winfo_screenheight()
    x, y = int(scr_width * 0.5 - width * 0.5), int(scr_height * 0.5 - height * 0.5)
    master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    e = ttk.Entry(master)
    e.focus_set()
    # e.config(width=int(width * 0.7))    # This width is in character, not pixel.
    e.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER, width=int(width * 0.7))

    result = None

    def callback(event=None):
        nonlocal result
        result = e.get()
        master.destroy()

    def callback_cancel(event=None):
        nonlocal result
        result = None
        master.destroy()

    master.bind('<Return>', callback)
    master.bind('<Escape>', callback_cancel)

    b = ttk.Button(master, text='OK', width=10, command=callback)
    b.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    master.mainloop()

    return result


__all__ = [
    'Colors', 'alpha_color',
    'get_width', 'get_height', 'pos', 'pos_x', 'pos_y',
    'get_sprite_box', 'get_label_box',
    'try_load_image',
    'try_add', 'try_remove',
    'set_menu_style',
    'DefaultLabelStyle',
    'hs_style_label',
    'NoticeLabel', 'notice',
    'popup_input'
]
