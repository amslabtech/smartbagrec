from __future__ import annotations

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk
from typing import List, Tuple

from modules.widgets import (Button, Checkbutton, Entry, Frame, Label,
                             Labelframe, MainWindow, ModalWindow, Pos,
                             Radiobutton, ScrollableListbox)


class SmartBagRec(MainWindow):
    outer_frame: OuterFrame

    def __init__(self, title: str) -> None:
        super().__init__(title)
        self.parent: None
        self.tk_widget: tk.Tk

        self.tk_widget.geometry("960x540")
        self.outer_frame = OuterFrame(self, (0, 0), {"padx": 8, "pady": 8, "sticky": "nsew"})

        print("[SmartBagRec] Initialized application.")

    def open_profile(self) -> None:
        self.outer_frame.bagrec_frame.on_clicked_load_from_profile_button()
        self.tk_widget.mainloop()

    def __del__(self) -> None:
        print("[SmartBagRec] Normally terminated application.")


class OuterFrame(Frame):
    topic_list_frame: TopicListFrame
    settings_frame: SettingsFrame
    save_mode_frame: SaveModeFrame
    bagrec_frame: BagRecFrame

    def __init__(self, parent: SmartBagRec, pos: Pos, grid_opt: dict = {}) -> None:
        super().__init__(parent, pos, grid_opt)
        self.parent: SmartBagRec
        self.tk_widget: ttk.Frame

        self.topic_list_frame = TopicListFrame(
            self, (0, 0), {"rowspan": 3, "padx": 8, "pady": 8, "sticky": "nsew"})
        self.settings_frame = SettingsFrame(
            self, (0, 1), {"padx": 8, "pady": 8, "sticky": "new"})
        self.save_mode_frame = SaveModeFrame(
            self, (1, 1), {"padx": 8, "pady": 8, "sticky": "ew"})
        self.bagrec_frame = BagRecFrame(
            self, (2, 1), {"padx": 8, "pady": 8, "sticky": "ew"})


class TopicListFrame(Labelframe):
    topic_list: TopicList
    select_button_frame: SelectButtonFrame

    def __init__(self, parent: OuterFrame, pos: Pos, grid_opt: dict = {}) -> None:
        super().__init__(parent, "recording topics", pos, grid_opt)
        self.parent: OuterFrame
        self.tk_widget: ttk.Labelframe

        self.topic_list = TopicList(self, (0, 0, 0, 1), {"sticky": "nsew"})
        self.select_button_frame = SelectButtonFrame(self, (1, 0))


class SelectButtonFrame(Frame):
    reset_button: Button
    all_button: Button

    def __init__(self, parent: TopicListFrame, pos: Pos, grid_opt: dict = {}) -> None:
        super().__init__(parent, pos, grid_opt)
        self.parent: TopicListFrame
        self.tk_widget: ttk.Frame

        self.reset_button = Button(
            self, "reset", self.on_clicked_reset_button, (0, 0), {"padx": 4, "pady": 4})
        self.all_button = Button(
            self, "select all", self.on_clicked_all_button, (0, 1), {"padx": 4, "pady": 4})

    def on_clicked_reset_button(self) -> None:
        self.parent.topic_list.reset()

    def on_clicked_all_button(self) -> None:
        self.parent.topic_list.select_all()


class SettingsFrame(Labelframe):
    quiet_button: Checkbutton
    bz2_button: Checkbutton
    tcpnodelay_button: Checkbutton
    split_button: Checkbutton
    size_button: Checkbutton
    size_entry: Entry
    duration_button: Checkbutton
    duration_entry: Entry
    advenced_settings_button: Button
    advenced_settings_window: AdvencedSettingsWindow

    def __init__(self, parent: OuterFrame, pos: Pos, grid_opt: dict = {}) -> None:
        super().__init__(parent, "settings for recording", pos, grid_opt)
        self.parent: OuterFrame
        self.tk_widget: ttk.Labelframe

        button_grid_opt = {"sticky": "wn"}
        self.quiet_button = Checkbutton(
            self, "suppress console output", (0, 0), button_grid_opt)
        self.bz2_button = Checkbutton(
            self, "use BZ2 compression", (1, 0), button_grid_opt)
        self.tcpnodelay_button = Checkbutton(
            self, "use the TCP_NODELAY transport hint when subscribing to topics", (2, 0), button_grid_opt)
        self.split_button = Checkbutton(
            self, "split the bag when maximum size or duration is reached", (3, 0), button_grid_opt)
        self.size_button = Checkbutton(
            self, "record a bag of maximum size SIZE MB (Default: infinite)", (4, 0), button_grid_opt)
        self.size_entry = Entry(self, (4, 1), {"padx": 4, "pady": 4, "sticky": "we"})
        self.duration_button = Checkbutton(
            self, "record a bag of maximum duration DURATION in seconds,\nunless 'm', or 'h' is appended",
            (5, 0), button_grid_opt)
        self.duration_entry = Entry(self, (5, 1), {"padx": 4, "pady": 4, "sticky": "we"})
        self.advenced_settings_button = Button(
            self, "advanced settings", self.on_clicked_advenced_settings_button, (6, 1), {"padx": 4, "pady": 4})
        self.advenced_settings_window = AdvencedSettingsWindow(
            self, self.parent.parent.tk_widget, "advanced settings")
        self.advenced_settings_window.on_close()

    def on_clicked_advenced_settings_button(self) -> None:
        self.advenced_settings_window.tk_widget.deiconify()


class AdvencedSettingsWindow(ModalWindow):
    publish_button: Checkbutton
    lz4_button: Checkbutton
    udp_button: Checkbutton
    repeat_latched_button: Checkbutton
    buffer_size_button: Checkbutton
    buffer_size_entry: Entry
    chunk_size_button: Checkbutton
    chunk_size_entry: Entry
    limit_button: Checkbutton
    limit_entry: Entry
    node_button: Checkbutton
    node_entry: Entry

    def __init__(self, parent: SettingsFrame, master: tk.Tk, title: str) -> None:
        super().__init__(parent, master, title)
        self.parent: SettingsFrame
        self.tk_widget: tk.Toplevel

        button_grid_opt = {"sticky": "wn"}
        self.publish_button = Checkbutton(
            self, "publish a msg when the record begin", (0, 0), button_grid_opt)
        self.lz4_button = Checkbutton(
            self, "use LZ4 compression", (1, 0), button_grid_opt)
        self.udp_button = Checkbutton(
            self, "use the UDP transport hint when subscribing to topics", (2, 0), button_grid_opt)
        self.repeat_latched_button = Checkbutton(
            self, "repeat latched msgs at the start of each new bag file", (3, 0), button_grid_opt)
        self.max_splits_button = Checkbutton(
            self,
            "keep a maximum of N bag files,\n" +
            "when reaching the maximu erase the oldest one\n" +
            "to keep a constant number of files",
            (4, 0), button_grid_opt)
        self.max_splits_entry = Entry(self, (4, 1), {"padx": 4, "pady": 4, "sticky": "we"})
        self.buffer_size_button = Checkbutton(
            self, "use an internal buffer of size SIZE MB\n(Default: 256, 0 = infinite)",
            (5, 0), button_grid_opt)
        self.buffer_size_entry = Entry(self, (5, 1), {"padx": 4, "pady": 4, "sticky": "we"})
        self.chunk_size_button = Checkbutton(
            self, "record to chunks of SIZE KB (Default: 768) (advanced)", (6, 0), button_grid_opt)
        self.chunk_size_entry = Entry(self, (6, 1), {"padx": 4, "pady": 4, "sticky": "we"})
        self.limit_button = Checkbutton(
            self, "only record NUM messages on each topic", (7, 0), button_grid_opt)
        self.limit_entry = Entry(self, (7, 1), {"padx": 4, "pady": 4, "sticky": "we"})
        self.node_button = Checkbutton(
            self, "record all topics subscribed to by a specific node", (8, 0), button_grid_opt)
        self.node_entry = Entry(self, (8, 1), {"padx": 4, "pady": 4, "sticky": "we"})

        self.tk_widget.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self) -> None:
        self.parent.parent.parent.tk_widget.grab_set()
        self.tk_widget.withdraw()


class SaveModeFrame(Labelframe):
    save_mode: tk.IntVar
    set_default_button: Radiobutton
    set_prefix_button: Radiobutton
    set_name_button: Radiobutton
    cwd_label: Label
    prefix_entry: Entry
    name_label: Label
    open_name_dialog_button: Button
    file_name: str

    def __init__(self, parent: OuterFrame, pos: Pos, grid_opt: dict = {}) -> None:
        super().__init__(parent, "select save mode", pos, grid_opt)
        self.parent: OuterFrame
        self.tk_widget: ttk.Labelframe

        self.save_mode = tk.IntVar()
        self.set_default_button = Radiobutton(
            self, "save to current dir", self.save_mode, 0, self.on_clicked_set_default_button,
            (0, 0), {"padx": 4, "pady": 4, "sticky": "w"})
        self.set_prefix_button = Radiobutton(
            self, "set prefix", self.save_mode, 1, self.on_clicked_set_prefix_button,
            (1, 0), {"padx": 4, "pady": 4, "sticky": "w"})
        self.set_name_button = Radiobutton(
            self, "set file path", self.save_mode, 2, self.on_clicked_set_name_button,
            (2, 0), {"padx": 4, "pady": 4, "sticky": "w"})

        self.cwd_label = Label(
            self, os.getcwd(), (0, 1), {"columnspan": 2, "padx": 4, "pady": 4, "sticky": "ew"})
        self.prefix_entry = Entry(
            self, (1, 1), {"columnspan": 2, "padx": 4, "pady": 4, "sticky": "ew"})
        self.name_label = Label(
            self, "./example.bag", (2, 1), {"padx": 4, "pady": 4, "sticky": "ew"})
        self.open_name_dialog_button = Button(
            self, "brouse", self.on_clicked_open_name_dialog_button,
            (2, 2), {"padx": 4, "pady": 4, "sticky": "ew"})

        self.file_name = "./example.bag"
        self.prefix_entry.tk_widget["state"] = tk.DISABLED
        self.open_name_dialog_button.tk_widget["state"] = tk.DISABLED

    def on_clicked_set_default_button(self) -> None:
        self.open_name_dialog_button.tk_widget["state"] = tk.DISABLED
        self.prefix_entry.tk_widget["state"] = tk.DISABLED

    def on_clicked_set_prefix_button(self) -> None:
        self.open_name_dialog_button.tk_widget["state"] = tk.DISABLED
        self.prefix_entry.tk_widget["state"] = tk.NORMAL

    def on_clicked_set_name_button(self) -> None:
        self.open_name_dialog_button.tk_widget["state"] = tk.NORMAL
        self.prefix_entry.tk_widget["state"] = tk.DISABLED

    def on_clicked_open_name_dialog_button(self) -> None:
        self.file_name = filedialog.asksaveasfilename(initialdir=".")
        self.name_label.tk_widget.configure(text=self.file_name)  # type: ignore
        if self.file_name == "":
            self.file_name = "./example.bag"
            self.name_label.tk_widget.configure(text="./example.bag")  # type: ignore


class BagRecFrame(Frame):
    record_button: Button
    save_as_profile_button: Button
    load_from_profile_button: Button
    rosbag_record_process: subprocess.Popen
    recording_window: RecordingWindow

    def __init__(self, parent: OuterFrame, pos: Pos, grid_opt: dict = {}) -> None:
        super().__init__(parent, pos, grid_opt)
        self.parent: OuterFrame
        self.tk_widget: ttk.Frame
        self.save_as_profile_button = Button(
            self, "save as profile", self.on_clicked_save_as_profile_button, (0, 0), {"padx": 4, "pady": 8, "sticky": "ew"})
        self.load_from_profile_button = Button(
            self, "load from profile", self.on_clicked_load_from_profile_button, (1, 0), {"padx": 4, "pady": 8, "sticky": "ew"})
        self.record_button = Button(
            self, "record", self.on_clicked_record_button, (2, 0), {"padx": 4, "pady": 8, "sticky": "ew"})

    def generate_rosbag_record_command(self) -> List[str]:
        command = ["rosbag", "record"]

        if self.parent.settings_frame.bz2_button.get_state():
            command.append("-j")
        if self.parent.settings_frame.advenced_settings_window.lz4_button.get_state():
            command.append("--lz4")
        if self.parent.settings_frame.split_button.get_state():
            if (self.parent.settings_frame.duration_button.get_state()
                    or self.parent.settings_frame.size_button.get_state()):
                command.append("--split")
        if self.parent.settings_frame.advenced_settings_window.publish_button.get_state():
            command.append("-p")
        if self.parent.settings_frame.quiet_button.get_state():
            command.append("-q")
        if self.parent.settings_frame.advenced_settings_window.repeat_latched_button.get_state():
            command.append("--repeat-latched")
        if self.parent.settings_frame.tcpnodelay_button.get_state():
            command.append("--tcpnodelay")
        if self.parent.settings_frame.advenced_settings_window.udp_button.get_state():
            command.append("--udp")

        if self.parent.settings_frame.size_button.get_state():
            state = self.parent.settings_frame.size_entry.get_state()
            if not state:
                state = "0"
            command.append("--size")
            command.append(state)
        if self.parent.settings_frame.duration_button.get_state():
            state = self.parent.settings_frame.duration_entry.get_state()
            if not state:
                state = "99h"
            command.append("--duration")
            command.append(state)
        if self.parent.settings_frame.advenced_settings_window.max_splits_button.get_state():
            state = self.parent.settings_frame.advenced_settings_window.max_splits_entry.get_state()
            if not state:
                state = "0"
            command.append("--max-splits")
            command.append(state)
        if self.parent.settings_frame.advenced_settings_window.buffer_size_button.get_state():
            state = self.parent.settings_frame.advenced_settings_window.buffer_size_entry.get_state()
            if not state:
                state = "256"
            command.append("-b")
            command.append(state)
        if self.parent.settings_frame.advenced_settings_window.chunk_size_button.get_state():
            state = self.parent.settings_frame.advenced_settings_window.chunk_size_entry.get_state()
            if not state:
                state = "768"
            command.append("--chunksize")
            command.append(state)
        if self.parent.settings_frame.advenced_settings_window.limit_button.get_state():
            state = self.parent.settings_frame.advenced_settings_window.limit_entry.get_state()
            if not state:
                state = "0"
            command.append("--limit")
            command.append(state)
        if self.parent.settings_frame.advenced_settings_window.node_button.get_state():
            state = self.parent.settings_frame.advenced_settings_window.node_entry.get_state()
            if state:
                command.append("--node")
                command.append(state)

        if self.parent.save_mode_frame.save_mode.get() == 1:
            command.append("-o")
            command.append(self.parent.save_mode_frame.prefix_entry.get_state())
        elif self.parent.save_mode_frame.save_mode.get() == 2:
            command.append("-O")
            command.append(self.parent.save_mode_frame.file_name)

        topics = (self.parent
                      .topic_list_frame
                      .topic_list
                      .get_selected())
        if not topics:
            return []
        command.extend(topics)

        return command

    def open_record_process(self, command) -> None:
        print(f"[SmartBagRec] Recording command is: {' '.join(command)}")
        self.rosbag_record_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.recording_window = RecordingWindow(self, self.parent.parent.tk_widget, "recording")  # type: ignore

    def on_clicked_save_as_profile_button(self) -> None:
        command = self.generate_rosbag_record_command()
        if not command:
            return
        default_dir = os.environ["HOME"] + "/.config/smartbagrec"
        os.makedirs(default_dir, exist_ok=True)
        file_name = filedialog.asksaveasfilename(initialdir=default_dir, initialfile="default.profile")
        with open(file_name, "w") as f:
            f.write(" ".join(command))
        print("[SmartBagRec] Saved as profile: " + file_name)

    def on_clicked_load_from_profile_button(self) -> None:
        default_dir = os.environ["HOME"] + "/.config/smartbagrec"
        os.makedirs(default_dir, exist_ok=True)
        file_name = filedialog.askopenfilename(initialdir=default_dir)
        if not file_name:
            return
        with open(file_name, "r") as f:
            command = f.readline()
            if ("rosbag record" in command and
                    ";" not in command and
                    "|" not in command and
                    "&" not in command):
                print("[SmartBagRec] Loaded from profile: " + file_name)
                self.open_record_process(command.split())

    def on_clicked_record_button(self) -> None:
        command = self.generate_rosbag_record_command()
        if not command:
            return
        self.open_record_process(command)


class TopicList(ScrollableListbox):

    def __init__(self, parent: TopicListFrame, pos: Pos, grid_opt: dict = {}) -> None:
        super().__init__(parent, self.fetch_topics(), "multiple", pos, grid_opt)
        self.parent: TopicListFrame
        self.tk_widget: tk.Listbox

    def select_all(self) -> None:
        self.tk_widget: tk.Listbox
        self.tk_widget.select_set(0, tk.END)

    def reset(self) -> None:
        self.tk_widget: tk.Listbox
        self.tk_widget.selection_clear(0, tk.END)

    @staticmethod
    def fetch_topics() -> Tuple[str]:
        return tuple(subprocess.run(
            ["rostopic", "list"], capture_output=True, text=True).stdout.split())


class RecordingWindow(ModalWindow):
    _recording_frame: Frame

    def __init__(self, parent: BagRecFrame, master: tk.Tk, title: str) -> None:
        super().__init__(parent, master, title)
        self.parent: BagRecFrame
        self.tk_widget: tk.Toplevel

        self._recording_frame = RecordingFrame(self, (0, 0), {"padx": 8, "pady": 8})
        self.tk_widget.protocol("WM_DELETE_WINDOW", self.on_close)

    def kill_rosbag_record_process(self) -> None:
        ret = subprocess.run(["kill", "-0", str(self.parent.rosbag_record_process.pid)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ret.returncode == 0:
            subprocess.run(["kill", "-TERM", str(self.parent.rosbag_record_process.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("[SmartBagRec] Recording has been stopped.")

    def __del__(self) -> None:
        self.kill_rosbag_record_process()

    def on_close(self) -> None:
        self.kill_rosbag_record_process()
        self.tk_widget.destroy()


class RecordingFrame(Frame):
    _recording_label: Label
    _recording_sec: int

    def __init__(self, parent: RecordingWindow, pos: Pos, grid_opt: dict = {}) -> None:
        super().__init__(parent, pos, grid_opt)
        self.parent: RecordingWindow
        self.tk_widget: ttk.Frame

        self._recording_sec = 0
        text = ("Recording bag file..." + "\n" +
                "Close this window to stop recording." + "\n\n"
                "(00:00)")
        self._recording_label = Label(self, text, (0, 0), {"padx": 4, "pady": 4})
        self._recording_label.tk_widget.after(1000, self._timer_callback)

    def _timer_callback(self) -> None:
        if self.parent.parent.rosbag_record_process.poll() == 0:
            self.parent.tk_widget.destroy()
            print("[SmartBagRec] Recording has been stopped.")
            return
        elif self.parent.parent.rosbag_record_process.poll():
            text = ("Something went wrong during recording." + "\n" +
                    "Causes may be:" + "\n\n" +
                    self.parent.parent.rosbag_record_process.stderr.read().decode("utf-8"))  # type: ignore
            self._recording_label.tk_widget.configure(text=text)  # type: ignore
            print("[SmartBagRec]", text)
            return

        self._recording_sec += 1
        text = ("Recording bag file..." + "\n" +
                "Close this window to stop recording." + "\n\n"
                f"({self._recording_sec // 60 :02d}:{self._recording_sec % 60 :02d})")
        self._recording_label.tk_widget.configure(text=text)  # type: ignore
        self._recording_label.tk_widget.after(1000, self._timer_callback)
