#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import os
import subprocess
import tempfile
import appindicator
import gtk
import cairo

import cream

KEYMAPS = [
        {
            'id': 'de',
            'exec': 'setxkbmap de'
        },
        {
            'id': 'gr',
            'exec': 'setxkbmap -layout gr -variant deadacute,polytonic'
        }
    ]
ACTION_TOGGLE_KEYBOARD_LAYOUT = 'toggle-keyboard-layout' 

class KeyboardManager(cream.Module):
    
    def __init__(self):
        
        cream.Module.__init__(self, 'org.sbillaudelle.KeyboardManager')
        
        self.active_layout = 0
        
        self.hotkeys.connect('hotkey-activated', self.hotkey_activated_cb)
        
        self.indicator = appindicator.Indicator(self.context.manifest['name'], "/usr/share/icons/cream/scalable/widgets/stopwatch/stop-watch.svg", appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        
        self.menu = gtk.Menu()
        
        self.settings_item = gtk.ImageMenuItem(stock_id=gtk.STOCK_PREFERENCES)
        self.settings_item.connect('activate', lambda *args: self.config.show_dialog())
        self.menu.append(self.settings_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        
        self.set_layout(0)
        
        
    def generate_icon_for_layout(self, n):
        
        s = KEYMAPS[n]['id']
        
        path = tempfile.mktemp(suffix='.png')

        surface = cairo.ImageSurface.create_from_png(os.path.join(self.context.get_path(), 'data/keyboard.png'))
        ctx = cairo.Context(surface)
        ctx.set_font_size(10)

        x_bearing, y_bearing, width, height = ctx.text_extents(s)[:4]
        ctx.move_to((22 - width) / 2, 10 - (5 - height) / 2)
        ctx.show_text(s)
        ctx.stroke()
        surface.write_to_png(path)
        return path
        
        
    def set_layout(self, n):
        
        icon = self.generate_icon_for_layout(n)
        self.indicator.set_icon(icon)
        
        l = KEYMAPS[n]
        subprocess.call(l['exec'].split(' '))
        
        
    def hotkey_activated_cb(self, manager, action):
        
        if action == ACTION_TOGGLE_KEYBOARD_LAYOUT:
            self.active_layout += 1
            if self.active_layout >= len(KEYMAPS):
                self.active_layout = 0
            self.set_layout(self.active_layout)
        
        
if __name__ == '__main__':
    keyboard_manager = KeyboardManager()
    keyboard_manager.main()
