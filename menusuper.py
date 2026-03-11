#!/usr/bin/env python3
import sys
import gi
import subprocess

current_menu_window = None

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf


class MenuWindow(Gtk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_border_width(0)
        self.set_app_paintable(True)
        self.set_visual(self.get_screen().get_rgba_visual())
        self.set_default_size(80, 200)   # ← LA LIGNE QUI RÈGLE TOUT
        self.connect("focus-out-event", lambda w, e: self.close())

        css = b"""
.menucontainer {
    background-color: rgba(0, 0, 0, 0.95);
    border-radius: 14px;
    padding: 10px;
}

button {
    padding: 0;
    min-width: 0;
    min-height: 0;
}

button,
button * {
    background: none;
    border: none;
    box-shadow: none;
}
"""
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        outer.get_style_context().add_class("menucontainer")
        outer.set_homogeneous(False)
        self.add(outer)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_homogeneous(False)
        outer.pack_start(box, False, False, 0)

        # ----------------------------------------------------
        # BOUTON 1
        # ----------------------------------------------------
        btn1 = Gtk.Button()
        btn1.set_size_request(40, 40)
        pix1 = GdkPixbuf.Pixbuf.new_from_file_at_size(
            "/usr/share/icons/SimpleOS-icons/scalable/apps/aide.svg",
            24, 24
        )
        img1 = Gtk.Image.new_from_pixbuf(pix1)
        btn1.add(img1)
        btn1.connect("clicked", lambda w: subprocess.Popen(["pcmanfm"]))
        box.pack_start(btn1, False, False, 0)

        # ----------------------------------------------------
        # BOUTON 2
        # ----------------------------------------------------
        btn2 = Gtk.Button()
        btn2.set_size_request(40, 40)
        pix2 = GdkPixbuf.Pixbuf.new_from_file_at_size(
            "/usr/share/icons/SimpleOS-icons/scalable/apps/aide.svg",
            24, 24
        )
        img2 = Gtk.Image.new_from_pixbuf(pix2)
        btn2.add(img2)
        btn2.connect("clicked", lambda w: subprocess.Popen(["aide"]))
        box.pack_start(btn2, False, False, 0)

        # ----------------------------------------------------
        # BOUTON 3
        # ----------------------------------------------------
        btn3 = Gtk.Button()
        btn3.set_size_request(40, 40)
        pix3 = GdkPixbuf.Pixbuf.new_from_file_at_size(
            "/usr/share/icons/SimpleOS-icons/scalable/apps/web-browser.svg",
            24, 24
        )
        img3 = Gtk.Image.new_from_pixbuf(pix3)
        btn3.add(img3)
        btn3.connect("clicked", lambda w: subprocess.Popen(["firefox"]))
        box.pack_start(btn3, False, False, 0)


class App(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        global current_menu_window
        if current_menu_window is not None:
            current_menu_window.destroy()
        
        win = MenuWindow(application=self)
        display = Gdk.Display.get_default()
        screen, x, y, _ = display.get_pointer()
        win.move(x, y)
        win.show_all()


if __name__ == "__main__":
    app = App()
    app.run(sys.argv)
