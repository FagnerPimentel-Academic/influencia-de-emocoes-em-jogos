import customtkinter as ctk
from PIL import Image, ImageTk
import datetime
import socket
import json
import os
from time import sleep
from redeNeural import realizarDeteccao
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Emotions")
root.geometry("1280x650")
root.configure(bg='#1e1e2d')

data = []

emotion1 = "sad"
emotion2 = "fear"

predicts = 10

import customtkinter as ctk

class CustomTable(ctk.CTkFrame):
    def __init__(self, parent, columns, data, width, height, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color="#1e1e2d", width=width, height=height)

        header_frame = ctk.CTkFrame(self, fg_color="#2e2e2e")
        header_frame.pack(fill="x")

        for col in columns:
            label = ctk.CTkLabel(header_frame, text=col, font=("Helvetica", 12, "bold"),
                                 text_color="white", fg_color="#2e2e2e",bg_color="#2e2e2e")
            label.pack(side="left", padx=1, pady=1, ipadx=43, ipady=5, expand=True)

        self.data_frame = ctk.CTkScrollableFrame(self, fg_color="#121212")
        self.data_frame.pack(fill="both", expand=True)

        self.update_data(data)

    def update_data(self, data):
        for widget in self.data_frame.winfo_children():
            widget.destroy()
        for row_data in data:
            row_frame = ctk.CTkFrame(self.data_frame, fg_color="#121212")
            row_frame.pack(fill="x", pady=2)

            for index, item in enumerate(row_data):
                if index == 2:
                    text_color = "green" if int(item)>=70 else "red"
                else:
                    text_color = "white"

                cell = ctk.CTkLabel(row_frame, text=item, font=("Helvetica", 12, "bold"),
                                    text_color=text_color, fg_color="#121212")
                cell.pack(side="left", padx=1, ipadx=1, ipady=5, expand=True)


def atualizar_indicador(emotion,count,accuracy_avg,resultTime,longest_time):
    emotions = { "happy": photo_felicidades_img, "fear": photo_medo_img, "neutral": photo_neutro_img, "sad": photo_tristeza_img, "angry": photo_raiva_img}  
    ctk.CTkLabel(frame_indicador, image=emotions[emotion], text="",bg_color="#121212").place(x=190, y=75)
    if emotion == 'neutral':
        ctk.CTkLabel(frame_indicador, text=f"                     ", text_color="green",bg_color="#121212",fg_color="#121212", font=("Poppins", 70, "bold")).place(x=40, y=225)
        ctk.CTkLabel(frame_indicador, text=f"                     ", text_color="green",bg_color="#121212",fg_color="#121212", font=("Poppins", 70, "bold")).place(x=40, y=300)
        ctk.CTkLabel(frame_indicador, text=f"                     ", text_color="green",bg_color="#121212",fg_color="#121212", font=("Poppins", 70, "bold")).place(x=40, y=325)
        ctk.CTkLabel(frame_indicador, text=f"                     ", text_color="green",bg_color="#121212",fg_color="#121212", font=("Poppins", 70, "bold")).place(x=40, y=350)
    elif count >= 0.7*predicts:
        ctk.CTkLabel(frame_indicador, text="Taxa de acerto:", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=250)
        ctk.CTkLabel(frame_indicador, text=f"{int((count/predicts)*100)}%     ", text_color="green",bg_color="#121212",fg_color="#121212", font=("Poppins", 70, "bold")).place(x=190, y=225)
    elif count >=0.5*predicts and count < 0.7*predicts:
        ctk.CTkLabel(frame_indicador, text="Taxa de acerto:", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=250)
        ctk.CTkLabel(frame_indicador, text=f"{int((count/predicts)*100)}%    ", text_color="yellow",bg_color="#121212",fg_color="#121212", font=("Poppins", 70, "bold")).place(x=190, y=225)
    else:
        ctk.CTkLabel(frame_indicador, text="Taxa de acerto:", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=250)
        ctk.CTkLabel(frame_indicador, text=f"{int((count/predicts)*100)}%     ", text_color="red",bg_color="#121212",fg_color="#121212", font=("Poppins", 70, "bold")).place(x=190, y=225)
    
    if emotion != 'neutral':
        ctk.CTkLabel(frame_indicador, text="Média de acurácia:", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=300)
        ctk.CTkLabel(frame_indicador, text=f"{round(accuracy_avg)}%", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=190, y=300)
        
        ctk.CTkLabel(frame_indicador, text="Média de tempo:", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=325)
        ctk.CTkLabel(frame_indicador, text=f"{round(resultTime)} ms", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=190, y=325)

        ctk.CTkLabel(frame_indicador, text="Maior tempo:", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=350)
        ctk.CTkLabel(frame_indicador, text=f"{round(longest_time)} ms", text_color="white",bg_color="#121212",fg_color="#121212", font=("Poppins", 14, "bold")).place(x=190, y=350)

def send_emotion(emotion:str,count,accuracy_avg,resultTime,longest_time):
    print(count)
    atualizar_indicador(emotion,count,accuracy_avg,resultTime,longest_time)
    data = {"emotion":emotion.upper()}
    json_data = json.dumps(data)
    HOST = '127.0.0.1'
    PORT = 65432

    sleep(1)
   
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json_data.encode('utf-8'))
    

def atualizar_table():
    table.update_data(data)


def process_emotion(emotion, opposite, response, count, resultTime):
    if float(response[emotion]) > float(response[opposite]):
        count += 1
        detected_emotion = emotion
    else:
        detected_emotion = opposite
    

    data.append((emotion, resultTime, response[emotion] * 100, detected_emotion))
    return count,(response[emotion]*100)

def on_click(emotion):
    def inner_on_click():
        now = datetime.datetime.now()
        hora_formatada = now.strftime("%H:%M:%S")
        count = 0

        emotion_pairs = {
            "sad": "happy",
            "happy": "sad",
            "fear": "angry",
            "angry": "fear"
        }


        accuracy_avg = 0
        time_avg = 0
        longest_time = 0
        if emotion == "neutral":
            data.append((emotion, 0, 100.0, emotion))
        else:
            for _ in range(predicts):
                start = time.time()
                response = realizarDeteccao(emotion)
                end = time.time()
                resultTime = round((end-start)*1000)
                time_avg += resultTime

                if resultTime > longest_time:
                    longest_time = resultTime

                if emotion in emotion_pairs:
                    opposite = emotion_pairs[emotion]
                    count,accurace = process_emotion(emotion, opposite, response, count, resultTime)
                    accuracy_avg += accurace

        if emotion == "neutral":
            send_emotion(emotion, predicts,100,0,0)
        elif count >= predicts/2:
            send_emotion(emotion, count,(accuracy_avg/predicts),time_avg/predicts,longest_time)
        else:
            opposite = emotion_pairs.get(emotion, None)
            if opposite:
                send_emotion(opposite, predicts - count,(accuracy_avg/predicts),time_avg/predicts,longest_time)

        atualizar_table()

    return inner_on_click


base_path = os.path.join(os.getcwd(), "redeNeural\\img")

# Emoções
emocoes_img = Image.open(os.path.join(base_path, "retangulo 1.png"))
photo_emocoes_img = ImageTk.PhotoImage(emocoes_img)

# Ondas
ondas_img = Image.open(os.path.join(base_path, "quadrado (1).png"))
photo_ondas_img = ImageTk.PhotoImage(ondas_img)

# Recentes
recentes_img = Image.open(os.path.join(base_path, "retangulo 2 (1).png"))
photo_recentes_img = ImageTk.PhotoImage(recentes_img)

# FEI
fei_img = Image.open(os.path.join(base_path, "fei.png"))
photo_fei_img = ImageTk.PhotoImage(fei_img)

# Felicidade
felicidade_img = Image.open(os.path.join(base_path, "felicidade.png"))
photo_felicidades_img = ImageTk.PhotoImage(felicidade_img)

# Tristeza
tristeza_img = Image.open(os.path.join(base_path, "tristeza.png"))
photo_tristeza_img = ImageTk.PhotoImage(tristeza_img)

# Medo
medo_img = Image.open(os.path.join(base_path, "medo.png"))
photo_medo_img = ImageTk.PhotoImage(medo_img)

# Raiva
raiva_img = Image.open(os.path.join(base_path, "raiva.png")) 
photo_raiva_img = ImageTk.PhotoImage(raiva_img)

# Neutro
neutro_img = Image.open(os.path.join(base_path, "neutro.png"))
photo_neutro_img = ImageTk.PhotoImage(neutro_img)

# Opções
opcoes_img = Image.open(os.path.join(base_path, "opções.png"))
photo_opcoes_img = ImageTk.PhotoImage(opcoes_img)

# Frames e componentes
frame_emocoes = ctk.CTkFrame(root, fg_color='#1a1a1a', width=800, height=500)
frame_emocoes.place(x=20, y=20)

ctk.CTkLabel(frame_emocoes, image=photo_emocoes_img, text="", fg_color='#1a1a1a').pack(anchor="w", padx=10, pady=5)

ctk.CTkLabel(frame_emocoes, text="Envio de Emoções", text_color="white", fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=20)

if emotion1 == "sad":
    btt_img = photo_tristeza_img
elif emotion1 == "happy":
    btt_img = photo_felicidades_img
elif emotion1 == "fear":
    btt_img = photo_medo_img
elif emotion1 == "angry":
    btt_img = photo_raiva_img

if emotion2 == "sad":
    btt_img2 = photo_tristeza_img
elif emotion2 == "happy":
    btt_img2 = photo_felicidades_img
elif emotion2 == "fear":
    btt_img2 = photo_medo_img
elif emotion2 == "angry":
    btt_img2 = photo_raiva_img

ctk.CTkButton(frame_emocoes, image=btt_img, text="",bg_color="#121212", fg_color="#121212", command=on_click(emotion1)).place(x=50, y=70)
ctk.CTkButton(frame_emocoes, image=btt_img2, text="",bg_color="#121212", fg_color="#121212", command=on_click(emotion2)).place(x=200, y=70)
ctk.CTkButton(frame_emocoes, image=photo_neutro_img, text="",bg_color="#121212", fg_color="#121212", command=on_click("neutral")).place(x=350, y=70)
ctk.CTkButton(frame_emocoes, image=photo_opcoes_img, text="",bg_color="#121212", fg_color="#121212").place(x=500, y=70)

frame_indicador = ctk.CTkFrame(root, fg_color='#1a1a1a', width=800, height=600)
frame_indicador.place(x=750, y=20)
ctk.CTkLabel(frame_indicador, image=photo_ondas_img, text="", text_color="white", font=("Helvetica", 14)).pack(anchor="w", padx=10, pady=5)
ctk.CTkLabel(frame_indicador, text="Emoção enviada", text_color="white", fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=20)
atualizar_indicador("neutral",predicts,100,0,0)

frame_lancamentos = ctk.CTkFrame(root, fg_color='#1a1a1a', width=690, height=500)
frame_lancamentos.place(x=20, y=300)

ctk.CTkLabel(frame_lancamentos, image=photo_recentes_img, text="", fg_color="#1a1a1a",bg_color="#121212").pack(anchor="w", padx=10, pady=5)

ctk.CTkLabel(frame_lancamentos, text="Lançados Recentemente", text_color="white", fg_color="#121212", font=("Poppins", 14, "bold")).place(x=40, y=40)

columns = ["Enviado", "Tempo (ms)", "Acurácia (%)", "Identificado"]
table = CustomTable(frame_lancamentos, columns, data, width=2000, height=800)
table.place(x=40, y=70)

frame_fei = ctk.CTkFrame(root, fg_color='#1a1a1a', width=690, height=500)
frame_fei.place(x=750, y=450)

ctk.CTkLabel(frame_fei, image=photo_fei_img, text="", text_color="white", font=("Helvetica", 14)).pack(anchor="w", padx=10, pady=5)

root.mainloop()
