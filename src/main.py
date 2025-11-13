from audio_text import AudioRecorder, AudioTextProcessor
from gemini_client import GeminiCallback
import threading
import customtkinter

customtkinter.set_appearance_mode("System") 
class sptGeminiApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.setup_form()

    def setup_form(self):
        self.title("SpeakToGemini")
        self.geometry("600x400")
        # 応答スペースの方が広がってほしいため，weight=0と設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.speakby_gemini_frame = SpeakbyGeminiFrame(self)
        self.speakby_gemini_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.input_text_frame = inputTextFrame(self,self.speakby_gemini_frame.update_textbox)
        self.input_text_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

class SpeakbyGeminiFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.geminicallback = GeminiCallback()
        self.setup_SGFform()

    def setup_SGFform(self):
        self.output_textbox = customtkinter.CTkTextbox(self, width=580)
        self.output_textbox.configure(state = "disabled")
        self.output_textbox.pack(expand = True, fill = customtkinter.Y,pady=10)

    def update_textbox(self,incoming_text):
        self.output_textbox.configure(state = "normal")
        reply = self.geminicallback.chat_withgemini(incoming_text)
        self.output_textbox.insert("end", f"{reply}")
        self.output_textbox.configure(state = "disabled")

class inputTextFrame(customtkinter.CTkFrame):
    def __init__(self, master, ex_func):
        super().__init__(master)
        self.audio_recorder = AudioRecorder()
        self.atp = AudioTextProcessor()
        self.ex_func= ex_func
        self.input_text = None
        self.setup_iTFform()

    def setup_iTFform(self):
        self.input_textbox = customtkinter.CTkTextbox(self, width=580, height=50)
        self.input_textbox.pack(side = customtkinter.LEFT,pady=10)
        self.record_button = customtkinter.CTkButton(self, text="録音開始", command=self.record_button_callback)
        self.record_button.pack(side = customtkinter.RIGHT,pady=10)
        self.send_button = customtkinter.CTkButton(self, text="送信", command=self.send_button_callback)
        self.send_button.pack(side = customtkinter.RIGHT,pady=10)

    def record_button_callback(self):
        if not self.audio_recorder.is_recording:
            self.record_button.configure(text="録音停止")
            self.recording_thread = threading.Thread(target=self.RecAndTextize,daemon=True)
            self.recording_thread.start()
        else:
            self.record_button.configure(text="録音開始")
            self.audio_recorder.stop()
    
    def send_button_callback(self):
        self.input_text = self.input_textbox.get("0.0", "end")
        self.input_textbox.delete("0.0", "end")
        self.ex_func(self.input_text)

    def RecAndTextize(self):
        self.audio_recorder.start()
        text = self.atp.speach_to_text("temp_audio_in.wav")
        self.input_textbox.insert("end", f"{text}\n")

if __name__ == "__main__":
    app = sptGeminiApp()
    app.mainloop()

