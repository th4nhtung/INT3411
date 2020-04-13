# Import the necessary modules.
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import tkinter.messagebox
import pyaudio
import wave
import os
import re

TOPIC = {
    'thoi-su': 'Thời sự',
    'goc-nhin': 'Góc nhìn',
    'the-gioi': 'Thế giới',
    'kinh-doanh': 'Kinh doanh',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'phap-luat': 'Pháp luật',
    'giao-duc': 'Giáo dục',
    'suc-khoe': 'Sức khoẻ',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch',
    'khoa-hoc': 'Khoa học',
    'so-hoa': 'Số hoá',
    'xe': 'Xe',
    'y-kien': 'Ý kiến',
    'tam-su': 'Tâm sự'
}
TOPIC_INFO = 'info.txt'
DATA_PATH = 'data'

class RecordAudio:
    def __init__(self, chunk=2048, format=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):
        # Start Tkinter and set Title
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry('800x480')
        self.main.title('INT3411 - Speech Processing')
        self.CHUNK = chunk
        self.FORMAT = format
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.play = 0
        self.data_path = DATA_PATH
        self.info_file = TOPIC_INFO
        self.topic = tk.StringVar()
        self.topic.trace('w', self.load_topic)
        self.output = ''
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        # Set Frames
        self.topic_info = tkinter.Frame(self.main, padx=10, pady=10)
        self.content = tkinter.Frame(self.main, padx=10, pady=5)
        self.action_bar = tkinter.Frame(self.main, padx=10, pady=10)

        # Pack Frame
        self.topic_info.pack(side=tk.TOP)
        self.content.pack()
        self.action_bar.pack(side=tk.BOTTOM)

        # Topic info box
        ## Topic selection
        self.topic_box_lbl = tk.Label(self.topic_info, text="Topic:")
        self.topic_box_lbl.grid(row=0, column=0, padx=(0, 10))
        self.topic_box = ttk.Combobox(self.topic_info, values=list(TOPIC.values()), state="readonly", textvar=self.topic)
        self.topic_box.grid(row=0, column=1, padx=(0, 50))
        ## Topic URL
        self.topic_url_lbl = tk.Label(self.topic_info, text="URL:")
        self.topic_url_lbl.grid(row=0, column=2, padx=(0, 10))
        self.topic_url = tk.StringVar()
        self.topic_url_ent = tk.Entry(self.topic_info, width=60, state='readonly', textvariable=self.topic_url)
        self.topic_url_ent.grid(row=0, column=3)

        # Content box
        self.prev_content = scrolledtext.ScrolledText(self.content, width=90, height=7, wrap=tk.WORD, state=tk.DISABLED)
        self.prev_content.grid(row=0, column=0)
        self.content_box = scrolledtext.ScrolledText(self.content, width=90, height=7, wrap=tk.WORD, background='yellow', state=tk.DISABLED)
        self.content_box.grid(row=1, column=0)
        self.next_content = scrolledtext.ScrolledText(self.content, width=90, height=7, wrap=tk.WORD, state=tk.DISABLED)
        self.next_content.grid(row=2, column=0)

        # Action bar
        ## Previous sentence button
        self.prev_btn = tk.Button(self.action_bar, width=5, text='ᐊ', state=tk.DISABLED, command=lambda: self.goto_sentence(self.get_topic_key(), self.line_no, self.get_topic_key(), self.line_no - 1))
        self.prev_btn.grid(row=0, column=0)
        ## Progress bar: current sentence / total sentences
        self.progress = tk.Label(self.action_bar, width=5, text='0 / 0')
        self.progress.grid(row=0, column=1, padx=10)
        ## Next sentence button
        self.next_btn = tk.Button(self.action_bar, width=5, text='ᐅ', state=tk.DISABLED, command=lambda: self.goto_sentence(self.get_topic_key(), self.line_no, self.get_topic_key(), self.line_no + 1))
        self.next_btn.grid(row=0, column=2)
        ## Auto-next checkbox
        self.autonext_chk = tk.BooleanVar()
        self.autonext_chk.set(True)
        self.autonext = tk.Checkbutton(self.action_bar, text='Auto-next', var=self.autonext_chk)
        self.autonext.grid(row=0, column=3, padx=(15, 30))
        ## Record button
        self.action_btn = tk.Button(self.action_bar, width=10, padx=10, pady=5, text='Start Recording', command=lambda: self.start_record(), state=tk.DISABLED)
        self.action_btn.grid(row=0, column=4, padx=(0, 10), pady=5)
        ## Play button
        self.play_btn = tk.Button(self.action_bar, width=5, padx=10, pady=5, text='Play', command=lambda: self.play_audio(), state=tk.DISABLED)
        self.play_btn.grid(row=0, column=5, padx=(0, 10), pady=5)
        ## State (recording, playing)
        self.state_lbl = tk.Label(self.action_bar, width=35, text='Waiting for action ...')
        self.state_lbl.grid(row=0, column=6, padx=10)

        tkinter.mainloop()

    def change_btn_state(self, s, *args):
        for btn in args:
            btn['state'] = s

    def load_topic(self, *args):
        topic_key = self.get_topic_key()
        self.data = []
        with open(os.path.join(self.data_path, topic_key, self.info_file), 'r', encoding="utf-8") as f:
            line_no = 0
            line_data = []
            pattern = re.compile("Link: (.*?)\\n")
            for line in f.readlines():
                if (line_no == 0): # topic url
                    url = pattern.search(line).group(1)
                    self.topic_url.set(url)
                else:
                    line_data.append(line.strip(' \t\n\r'))
                    if (line_no == 2): # sentence
                        self.data.append(line_data)
                        line_data = []
                line_no = 1 if (line_no == 0) else 3 - line_no
        self.line_no = 0 # NOTE: LINE_NO START FROM 0
        self.goto_sentence('', 0, topic_key, 0)

    def get_topic_key(self):
        return [k for (k, v) in TOPIC.items() if v == self.topic.get()][0];

    def goto_sentence(self, _t, _s, t, s):
        self.action_btn.configure(text='Start Recording', command=self.start_record, state=tk.NORMAL)
        self.change_btn_state(tk.NORMAL, self.topic_box, self.play_btn)
        self.state_lbl['text'] = 'Waiting for action ...'
        if (t != _t):
            self.topic.set(TOPIC[t])
        self.line_no = s
        self.prev_btn['state'] = tk.NORMAL if (s > 0) else tk.DISABLED
        self.update_content(self.prev_content, self.data[s - 1][1] if (s > 0) else '')
        self.next_btn['state'] = tk.NORMAL if (s < len(self.data) - 1) else tk.DISABLED
        self.update_content(self.next_content, self.data[s + 1][1] if (s < len(self.data) - 1) else '')
        self.update_content(self.content_box, self.data[s][1])
        self.progress['text'] = '{:d} / {:d}'.format(self.line_no + 1, len(self.data))
        self.output = self.data[s][0]

    def play_audio(self):
        self.play = 1
        audio_file = os.path.join(self.get_topic_key(), self.output)
        audio_full_path = os.path.join(self.data_path, audio_file)
        file_exists = os.path.exists(audio_full_path) and os.path.isfile(audio_full_path)
        self.state_lbl['text'] = 'Playing {:s} ...'.format(audio_file) if (file_exists) else 'File {:s} not found!'.format(audio_file)
        if (not file_exists): return
        self.change_btn_state(tk.DISABLED, self.topic_box, self.prev_btn, self.next_btn, self.action_btn)
        self.play_btn.configure(text='Stop', command=self.stop_audio)
        wf = wave.open(audio_full_path, 'rb')
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
        data = wf.readframes(self.CHUNK)
        while self.play == 1 and len(data) > 0:
            stream.write(data)
            data = wf.readframes(self.CHUNK)
            self.main.update()

        stream.stop_stream()
        stream.close()

        self.change_btn_state(tk.NORMAL, self.topic_box, self.prev_btn, self.next_btn, self.action_btn)
        self.play_btn.configure(text='Play', command=self.play_audio)
        self.state_lbl['text'] = 'Waiting for action ...'

    def stop_audio(self):
        self.play = 0

    def update_content(self, t, c):
        t['state'] = tk.NORMAL
        t.delete(1.0, tk.END)
        t.insert(tk.END, c)
        t['state'] = tk.DISABLED

    def start_record(self):
        self.st = 1
        self.frames = []
        self.change_btn_state(tk.DISABLED, self.topic_box, self.prev_btn, self.next_btn, self.play_btn)
        self.action_btn.configure(text='Stop Recording', command=self.stop_record)
        output_target = os.path.join(self.get_topic_key(), self.output)
        self.state_lbl['text'] = 'Recording to {:s} ...'.format(output_target)
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            self.main.update()
        stream.close()

        wf = wave.open(os.path.join(self.data_path, output_target), 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        _ln = self.line_no
        self.line_no += 1 if (self.autonext_chk.get() and self.line_no < len(self.data) - 1) else 0
        self.goto_sentence(self.topic, _ln, self.topic, self.line_no)

    def stop_record(self):
        self.st = 0

# Create an object of the ProgramGUI class to begin the program.
if __name__ == '__main__':
    guiAudio = RecordAudio()