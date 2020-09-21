import sys
from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import time
import os
import matplotlib.pyplot as plt
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader
from camera import Camera
from tkinter import filedialog
from ClassParams import Struct




root = Tk()
root.title('DC Motor')
root.geometry("400x600")
root.configure(background='#CCFFE5')

structs = []

voltage_manual = 0
moi_manual = 0
res_manual = 0
induc_manual = 0
damping_manual = 0
ct_manual = 0

i_deriv = 0
w_deriv = 0
i_current = 0
w_current = 0
i_old = 0
i_deriv_old = 0
w_old = 0
w_deriv_old = 0
curr_index = 0

current_time = 0

i_vector = [0] * 9999999
w_vector = [0] * 9999999
error = Label(root, text="Not all fields were completed or some fields do not \nrepresent numbers/valid numbers!",bg='#CCFFE5',fg='black')
error_voltage = Label(root, text="Voltage must be set!",bg='#CCFFE5',fg='black')


def calculate_index(index):
    global V
    global R
    global L
    global J
    global K
    global B
    if index == -1:
        V = float(Voltage_input.get())
        K = float(constant_input.get())
        B = float(damping_input.get())
        R = float(armature_resistance_input.get())
        L = float(armature_unductance_input.get())
        J = float(MOI_input.get())
    elif index == -2:
        V = float(voltage_manual)
        K = float(ct_manual)
        B = float(damping_manual)
        R = float(res_manual)
        L = float(induc_manual)
        J = float(moi_manual)
    else:
        V = float(structs[index].voltage)
        K = float(structs[index].constant)
        B = float(structs[index].damping)
        R = float(structs[index].resistance)
        L = float(structs[index].inductance)
        J = float(structs[index].moi)

    
    global i_deriv
    global w_deriv
    global i_current
    global w_current
    global i_old
    global i_deriv_old
    global w_old
    global w_deriv_old
    global curr_index
    global i_vector
    global w_vector

    if curr_index == 0:
        i_deriv = 0
        w_deriv = 0
        i_current = 0
        w_current = 0
        i_old = 0
        i_deriv_old = 0
        w_old = 0
        w_deriv_old = 0
        curr_index = 0

    i_vector[curr_index] = i_current
    curr_index += 1
    w_vector[curr_index - 1] = w_current

    w_deriv = (1/J) * (K * i_current - B * w_current)
    i_deriv = (1/L) * (V - R * i_current - K * w_current)
    i_current = i_deriv * pas + i_old - (i_deriv - i_deriv_old) * pas/2
    w_current = w_deriv * pas + w_old - (w_deriv - w_deriv_old) * pas/2


    i_old = i_current
    i_deriv_old = i_deriv
    w_old = w_current
    w_deriv_old = w_deriv

def current_index(index,index_sec):
    N = int(N_input.get()) * 100
    global current_time
    global pas
    global curr_index
    global i_vector


    curr_index = 0
    i_vector = [0] * N
    pas = 0.01
    x = [0] * N
    for i in range(0, N):
        calculate_index(index)
    curr_index = 0
    curr_index = 0
    current_time = 0
    for i in range(0, N):
        x[i] = current_time
        current_time += pas

    if index == -1 and index_sec != -2:
        plt.figure(figsize=(10,8))
        plt.plot(x,i_vector)
        plt.xlabel("Time(s)")
        plt.ylabel("Current Value(A)")
        plt.title('Current Intensity')  
        plt.text(3 * N/1000,0,"V = " + str(Voltage_input.get()))
        plt.text(4* N/1000,0,"J = " + str(MOI_input.get()))
        plt.text(5* N/1000,0,"R = " + str(armature_resistance_input.get()))
        plt.text(6* N/1000,0,"L = " + str(armature_unductance_input.get()))
        plt.text(7* N/1000,0,"B = " + str(damping_input.get()))
        plt.text(8* N/1000,0,"K = " + str(constant_input.get()))
        plt.show()
        return
    if index_sec == -1:
        plt.figure(figsize=(10,8))
        plt.plot(x, i_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Current Value(A)")
        plt.title('Current plot comparison')  
        plt.text(3 * N/1000,0,"V = " + str(structs[index].voltage),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(structs[index].moi),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(structs[index].resistance),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(structs[index].inductance),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(structs[index].damping),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(structs[index].constant),color='blue',fontsize=8)


        curr_index = 0
        i_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(-1)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas
        plt.plot(x, i_vector,'tab:red')
        plt.text(3 * N/1000,0.5,"V = " + str(Voltage_input.get()),color='red',fontsize=8)
        plt.text(4* N/1000,0.5,"J = " + str(MOI_input.get()),color='red',fontsize=8)
        plt.text(5* N/1000,0.5,"R = " + str(armature_resistance_input.get()),color='red',fontsize=8)
        plt.text(6* N/1000,0.5,"L = " + str(armature_unductance_input.get()),color='red',fontsize=8)
        plt.text(7* N/1000,0.5,"B = " + str(damping_input.get()),color='red',fontsize=8)
        plt.text(8* N/1000,0.5,"K = " + str(constant_input.get()),color='red',fontsize=8)
        plt.show()
        return
    if index >= 0 and index_sec >= 0:
        plt.figure(figsize=(10,8))
        plt.plot(x, i_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Current Value(A)")
        plt.title('Current plot comparison')  
        plt.text(3 * N/1000,0,"V = " + str(structs[index].voltage),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(structs[index].moi),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(structs[index].resistance),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(structs[index].inductance),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(structs[index].damping),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(structs[index].constant),color='blue',fontsize=8)


        curr_index = 0
        i_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(index_sec)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas

        plt.plot(x, i_vector,'tab:red')
        plt.text(3 * N/1000,0.5,"V = " + str(structs[index_sec].voltage),color='red',fontsize=8)
        plt.text(4* N/1000,0.5,"J = " + str(structs[index_sec].moi),color='red',fontsize=8)
        plt.text(5* N/1000,0.5,"R = " + str(structs[index_sec].resistance),color='red',fontsize=8)
        plt.text(6* N/1000,0.5,"L = " + str(structs[index_sec].inductance),color='red',fontsize=8)
        plt.text(7* N/1000,0.5,"B = " + str(structs[index_sec].damping),color='red',fontsize=8)
        plt.text(8* N/1000,0.5,"K = " + str(structs[index_sec].constant),color='red',fontsize=8)
        plt.show()
        return
    if index == -1 and index_sec == -2:
        plt.figure(figsize=(10,8))
        plt.plot(x, i_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Current Value(A)")
        plt.title('Current plot comparison') 
        plt.text(3 * N/1000,0,"V = " + str(Voltage_input.get()),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(MOI_input.get()),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(armature_resistance_input.get()),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(armature_unductance_input.get()),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(damping_input.get()),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(constant_input.get()),color='blue',fontsize=8)


        curr_index = 0
        i_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(index_sec)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas

        plt.plot(x, i_vector,'tab:red')
        plt.text(3 * N/1000,0.5,"V = " + str(voltage_manual),color='red',fontsize=8)
        plt.text(4* N/1000,0.5,"J = " + str(moi_manual),color='red',fontsize=8)
        plt.text(5* N/1000,0.5,"R = " + str(res_manual),color='red',fontsize=8)
        plt.text(6* N/1000,0.5,"L = " + str(induc_manual),color='red',fontsize=8)
        plt.text(7* N/1000,0.5,"B = " + str(damping_manual),color='red',fontsize=8)
        plt.text(8* N/1000,0.5,"K = " + str(ct_manual),color='red',fontsize=8)
        plt.show()
        return

def speed_theta(index,index_sec):
    N = int(N_input.get()) * 100
    global current_time
    global pas
    global curr_index
    global w_vector


    curr_index = 0
    w_vector = [0] * N
    pas = 0.01
    x = [0] * N
    for i in range(0, N):
        calculate_index(index)
    curr_index = 0
    current_time = 0
    for i in range(0, N):
        x[i] = current_time
        current_time += pas
    if index == -1 and index_sec != -2:
        plt.figure(figsize=(10,8))
        plt.plot(x,w_vector)
        plt.xlabel("Time(s)")
        plt.ylabel("Speed Value(rad/s)")
        plt.title('Speed')  
        plt.text(3* N/1000,0,"V = " + str(Voltage_input.get()))
        plt.text(4* N/1000,0,"J = " + str(MOI_input.get()))
        plt.text(5* N/1000,0,"R = " + str(armature_resistance_input.get()))
        plt.text(6* N/1000,0,"L = " + str(armature_unductance_input.get()))
        plt.text(7* N/1000,0,"B = " + str(damping_input.get()))
        plt.text(8* N/1000,0,"K = " + str(constant_input.get()))
        plt.show()
        return
    if index_sec == -1:
        plt.figure(figsize=(10,8))
        plt.plot(x,w_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Speed Value(rad/s)")
        plt.title('Speed comparison')  
        plt.text(3 * N/1000,0,"V = " + str(structs[index].voltage),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(structs[index].moi),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(structs[index].resistance),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(structs[index].inductance),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(structs[index].damping),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(structs[index].constant),color='blue',fontsize=8)


        curr_index = 0
        w_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(-1)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas

        plt.plot(x,w_vector,'tab:red')
        plt.text(3 * N/1000,1,"V = " + str(Voltage_input.get()),color='red',fontsize=8)
        plt.text(4* N/1000,1,"J = " + str(MOI_input.get()),color='red',fontsize=8)
        plt.text(5* N/1000,1,"R = " + str(armature_resistance_input.get()),color='red',fontsize=8)
        plt.text(6* N/1000,1,"L = " + str(armature_unductance_input.get()),color='red',fontsize=8)
        plt.text(7* N/1000,1,"B = " + str(damping_input.get()),color='red',fontsize=8)
        plt.text(8* N/1000,1,"K = " + str(constant_input.get()),color='red',fontsize=8)
        plt.show()
        return
    if index >= 0 and index_sec >= 0:
        plt.figure(figsize=(10,8))
        plt.plot(x,w_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Speed Value(rad/s)")
        plt.title('Speed comparison') 
        plt.text(3 * N/1000,0,"V = " + str(structs[index].voltage),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(structs[index].moi),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(structs[index].resistance),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(structs[index].inductance),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(structs[index].damping),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(structs[index].constant),color='blue',fontsize=8)


        curr_index = 0
        w_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(index_sec)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas

        plt.plot(x,w_vector,'tab:red')
        plt.text(3 * N/1000,1,"V = " + str(structs[index_sec].voltage),color='red',fontsize=8)
        plt.text(4* N/1000,1,"J = " + str(structs[index_sec].moi),color='red',fontsize=8)
        plt.text(5* N/1000,1,"R = " + str(structs[index_sec].resistance),color='red',fontsize=8)
        plt.text(6* N/1000,1,"L = " + str(structs[index_sec].inductance),color='red',fontsize=8)
        plt.text(7* N/1000,1,"B = " + str(structs[index_sec].damping),color='red',fontsize=8)
        plt.text(8* N/1000,1,"K = " + str(structs[index_sec].constant),color='red',fontsize=8)
        plt.show()
        return
    if index == -1 and index_sec == -2:
        plt.figure(figsize=(10,8))
        plt.plot(x,w_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Speed Value(rad/s)")
        plt.title('Speed comparison') 
        plt.text(3 * N/1000,0,"V = " + str(Voltage_input.get()),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(MOI_input.get()),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(armature_resistance_input.get()),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(armature_unductance_input.get()),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(damping_input.get()),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(constant_input.get()),color='blue',fontsize=8)


        curr_index = 0
        w_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(index_sec)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas

        plt.plot(x,w_vector,'tab:red')
        plt.text(3 * N/1000,1,"V = " + str(voltage_manual),color='red',fontsize=8)
        plt.text(4* N/1000,1,"J = " + str(moi_manual),color='red',fontsize=8)
        plt.text(5* N/1000,1,"R = " + str(res_manual),color='red',fontsize=8)
        plt.text(6* N/1000,1,"L = " + str(induc_manual),color='red',fontsize=8)
        plt.text(7* N/1000,1,"B = " + str(damping_manual),color='red',fontsize=8)
        plt.text(8* N/1000,1,"K = " + str(ct_manual),color='red',fontsize=8)
        plt.show()
        return
    

def torque_plot(index,index_sec):
    N = int(N_input.get()) * 100
    global current_time
    global pas
    global curr_index
    global i_vector


    curr_index = 0
    i_vector = [0] * N
    pas = 0.01
    x = [0] * N
    for i in range(0, N):
        calculate_index(index)
    curr_index = 0
    curr_index = 0
    current_time = 0
    for i in range(0, N):
        x[i] = current_time
        current_time += pas
    if index == -1:
        K = float(constant_input.get())
    else:
        K = float(structs[index].constant)

    for i in range(0,N):
        i_vector[i] *= K
    
    if index == -1 and index_sec != -2:
        plt.figure(figsize=(10,8))
        plt.plot(x,i_vector)
        plt.xlabel("Time(s)")
        plt.ylabel("Torque Value(N*m)")
        plt.title('Torque')  
        plt.text(3* N/1000,0,"V = " + str(Voltage_input.get()))
        plt.text(4* N/1000,0,"J = " + str(MOI_input.get()))
        plt.text(5* N/1000,0,"R = " + str(armature_resistance_input.get()))
        plt.text(6* N/1000,0,"L = " + str(armature_unductance_input.get()))
        plt.text(7* N/1000,0,"B = " + str(damping_input.get()))
        plt.text(8* N/1000,0,"K = " + str(constant_input.get()))
        plt.show()
        return
    if index_sec == -1:
        plt.figure(figsize=(10,8))
        plt.plot(x,i_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Torque Value(N*m)")
        plt.title('Torque comparison') 
        plt.text(3 * N/1000,0,"V = " + str(structs[index].voltage),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(structs[index].moi),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(structs[index].resistance),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(structs[index].inductance),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(structs[index].damping),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(structs[index].constant),color='blue',fontsize=8)


        curr_index = 0
        i_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(-1)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas
        K = float(constant_input.get())
        for i in range(0,N):
            i_vector[i] *= K

        plt.plot(x, i_vector,'tab:red')
        plt.text(3 * N/1000,0.5,"V = " + str(Voltage_input.get()),color='red',fontsize=8)
        plt.text(4* N/1000,0.5,"J = " + str(MOI_input.get()),color='red',fontsize=8)
        plt.text(5* N/1000,0.5,"R = " + str(armature_resistance_input.get()),color='red',fontsize=8)
        plt.text(6* N/1000,0.5,"L = " + str(armature_unductance_input.get()),color='red',fontsize=8)
        plt.text(7* N/1000,0.5,"B = " + str(damping_input.get()),color='red',fontsize=8)
        plt.text(8* N/1000,0.5,"K = " + str(constant_input.get()),color='red',fontsize=8)
        plt.show()
        return
    if index >= 0 and index_sec >= 0:
        plt.figure(figsize=(10,8))
        plt.plot(x,i_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Torque Value(N*m)")
        plt.title('Torque comparison') 
        plt.text(3 * N/1000,0,"V = " + str(structs[index].voltage),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(structs[index].moi),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(structs[index].resistance),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(structs[index].inductance),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(structs[index].damping),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(structs[index].constant),color='blue',fontsize=8)


        curr_index = 0
        i_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(index_sec)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas
        K = float(structs[index_sec].constant)
        for i in range(0,N):
            i_vector[i] *= K

        plt.plot(x, i_vector,'tab:red')
        plt.text(3 * N/1000,0.5,"V = " + str(structs[index_sec].voltage),color='red',fontsize=8)
        plt.text(4* N/1000,0.5,"J = " + str(structs[index_sec].moi),color='red',fontsize=8)
        plt.text(5* N/1000,0.5,"R = " + str(structs[index_sec].resistance),color='red',fontsize=8)
        plt.text(6* N/1000,0.5,"L = " + str(structs[index_sec].inductance),color='red',fontsize=8)
        plt.text(7* N/1000,0.5,"B = " + str(structs[index_sec].damping),color='red',fontsize=8)
        plt.text(8* N/1000,0.5,"K = " + str(structs[index_sec].constant),color='red',fontsize=8)
        plt.show()
        return
    if index == -1 and index_sec == -2:
        plt.figure(figsize=(10,8))
        plt.plot(x,i_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Torque Value(N*m)")
        plt.title('Torque comparison') 
        plt.text(3 * N/1000,0,"V = " + str(Voltage_input.get()),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(MOI_input.get()),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(armature_resistance_input.get()),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(armature_unductance_input.get()),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(damping_input.get()),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(constant_input.get()),color='blue',fontsize=8)


        curr_index = 0
        i_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(index_sec)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas
        K = float(ct_manual)
        for i in range(0,N):
            i_vector[i] *= K

        plt.plot(x, i_vector,'tab:red')
        plt.text(3 * N/1000,0.5,"V = " + str(voltage_manual),color='red',fontsize=8)
        plt.text(4* N/1000,0.5,"J = " + str(moi_manual),color='red',fontsize=8)
        plt.text(5* N/1000,0.5,"R = " + str(res_manual),color='red',fontsize=8)
        plt.text(6* N/1000,0.5,"L = " + str(induc_manual),color='red',fontsize=8)
        plt.text(7* N/1000,0.5,"B = " + str(damping_manual),color='red',fontsize=8)
        plt.text(8* N/1000,0.5,"K = " + str(ct_manual),color='red',fontsize=8)
        plt.show()
        return
    

def electromotive_force_plot(index,index_sec):
    N = int(N_input.get()) * 100
    global current_time
    global pas
    #global N
    global curr_index
    global w_vector


    curr_index = 0
    w_vector = [0] * N
    pas = 0.01
    x = [0] * N
    for i in range(0, N):
        calculate_index(index)
    curr_index = 0
    curr_index = 0
    current_time = 0
    for i in range(0, N):
        x[i] = current_time
        current_time += pas
    if index == -1:
        K = float(constant_input.get())
    else:
        K = float(structs[index].constant)
    for i in range(0,N):
        w_vector[i] *= K
    
    if index == -1 and index_sec != -2:
        plt.figure(figsize=(10,8))
        plt.plot(x,w_vector)
        plt.xlabel("Time(s)")
        plt.ylabel("Electromotive Force Value(V)")
        plt.title('Electromotive Force')  
        plt.text(3* N/1000,0,"V = " + str(Voltage_input.get()))
        plt.text(4* N/1000,0,"J = " + str(MOI_input.get()))
        plt.text(5* N/1000,0,"R = " + str(armature_resistance_input.get()))
        plt.text(6* N/1000,0,"L = " + str(armature_unductance_input.get()))
        plt.text(7* N/1000,0,"B = " + str(damping_input.get()))
        plt.text(8* N/1000,0,"K = " + str(constant_input.get()))
        plt.show()
        return
    if index_sec == -1:
        plt.figure(figsize=(10,8))
        plt.plot(x,w_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Electromotive Force Value(V)")
        plt.title('Electromotive Force Comparison') 
        plt.text(3 * N/1000,0,"V = " + str(structs[index].voltage),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(structs[index].moi),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(structs[index].resistance),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(structs[index].inductance),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(structs[index].damping),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(structs[index].constant),color='blue',fontsize=8)


        curr_index = 0
        w_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(-1)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas
        K = float(constant_input.get())
        for i in range(0,N):
            w_vector[i] *= K

        plt.plot(x,w_vector,'tab:red')
        plt.text(3 * N/1000,1,"V = " + str(Voltage_input.get()),color='red',fontsize=8)
        plt.text(4* N/1000,1,"J = " + str(MOI_input.get()),color='red',fontsize=8)
        plt.text(5* N/1000,1,"R = " + str(armature_resistance_input.get()),color='red',fontsize=8)
        plt.text(6* N/1000,1,"L = " + str(armature_unductance_input.get()),color='red',fontsize=8)
        plt.text(7* N/1000,1,"B = " + str(damping_input.get()),color='red',fontsize=8)
        plt.text(8* N/1000,1,"K = " + str(constant_input.get()),color='red',fontsize=8)
        plt.show()
        return
    if index >= 0 and index_sec >= 0:
        plt.figure(figsize=(10,8))
        plt.plot(x,w_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Electromotive Force Value(V)")
        plt.title('Electromotive Force Comparison') 
        plt.text(3 * N/1000,0,"V = " + str(structs[index].voltage),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(structs[index].moi),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(structs[index].resistance),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(structs[index].inductance),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(structs[index].damping),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(structs[index].constant),color='blue',fontsize=8)


        curr_index = 0
        w_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(index_sec)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas
        K = float(structs[index_sec].constant)
        for i in range(0,N):
            w_vector[i] *= K

        plt.plot(x,w_vector,'tab:red')
        plt.text(3 * N/1000,1,"V = " + str(structs[index_sec].voltage),color='red',fontsize=8)
        plt.text(4* N/1000,1,"J = " + str(structs[index_sec].moi),color='red',fontsize=8)
        plt.text(5* N/1000,1,"R = " + str(structs[index_sec].resistance),color='red',fontsize=8)
        plt.text(6* N/1000,1,"L = " + str(structs[index_sec].inductance),color='red',fontsize=8)
        plt.text(7* N/1000,1,"B = " + str(structs[index_sec].damping),color='red',fontsize=8)
        plt.text(8* N/1000,1,"K = " + str(structs[index_sec].constant),color='red',fontsize=8)
        plt.show()
        return
    if index == -1 and index_sec == -2:
        plt.figure(figsize=(10,8))
        plt.plot(x,w_vector,'tab:blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Electromotive Force Value(V)")
        plt.title('Electromotive Force Comparison') 
        plt.text(3 * N/1000,0,"V = " + str(Voltage_input.get()),color='blue',fontsize=8)
        plt.text(4* N/1000,0,"J = " + str(MOI_input.get()),color='blue',fontsize=8)
        plt.text(5* N/1000,0,"R = " + str(armature_resistance_input.get()),color='blue',fontsize=8)
        plt.text(6* N/1000,0,"L = " + str(armature_unductance_input.get()),color='blue',fontsize=8)
        plt.text(7* N/1000,0,"B = " + str(damping_input.get()),color='blue',fontsize=8)
        plt.text(8* N/1000,0,"K = " + str(constant_input.get()),color='blue',fontsize=8)


        curr_index = 0
        w_vector = [0] * N
        pas = 0.01
        x = [0] * N
        for i in range(0, N):
            calculate_index(index_sec)
        curr_index = 0
        curr_index = 0
        current_time = 0
        for i in range(0, N):
            x[i] = current_time
            current_time += pas
        K = float(ct_manual)
        for i in range(0,N):
            w_vector[i] *= K

        plt.plot(x,w_vector,'tab:red')
        plt.text(3 * N/1000,1,"V = " + str(voltage_manual),color='red',fontsize=8)
        plt.text(4* N/1000,1,"J = " + str(moi_manual),color='red',fontsize=8)
        plt.text(5* N/1000,1,"R = " + str(res_manual),color='red',fontsize=8)
        plt.text(6* N/1000,1,"L = " + str(induc_manual),color='red',fontsize=8)
        plt.text(7* N/1000,1,"B = " + str(damping_manual),color='red',fontsize=8)
        plt.text(8* N/1000,1,"K = " + str(ct_manual),color='red',fontsize=8)
        plt.show()
        return

def RepresentsInt(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def RepresentsInt_2(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def save_file(history):

    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
    filename = root.filename
    if not filename:
        return
    free_write = [0] * len(structs)
    try:
        f_read = open(filename, "r")
        while True: 
            line = f_read.readline()
            if not line: 
                break
            if "DC Motor Params" in line:

                voltage_file = f_read.readline().strip()
                MOI_file = f_read.readline().strip()
                armature_resistance_file = f_read.readline().strip()
                armature_unductance_file = f_read.readline().strip()
                damping_file = f_read.readline().strip()
                constant_file = f_read.readline().strip()
                for i in range(0,len(structs)):
                    if (float(voltage_file) == float(structs[i].voltage) and float(MOI_file) == float(structs[i].moi) and float(armature_resistance_file) == float(structs[i].resistance) and
                    float(armature_unductance_file) == float(structs[i].inductance) and float(damping_file) == float(structs[i].damping) and float(constant_file) == float(structs[i].constant)):
                        free_write[i] = 1
                        break

        f_read.close()
    except IOError:
        no_file = Label(history, text="File has to be created",bg='#CCFFE5',fg='black')
        no_file.pack()
        history.after(2000,no_file.pack_forget)
    nothing_written = 0
    for i in range(0,len(structs)):
        if free_write[i] == 0:
            nothing_written = 1
            f = open(filename, "a+")
        
            f.write("DC Motor Params\n")

            f.write(str(structs[i].voltage) + "\n")
            f.write(str(structs[i].moi) + "\n")
            f.write(str(structs[i].resistance) + "\n")
            f.write(str(structs[i].inductance) + "\n")
            f.write(str(structs[i].damping) + "\n")
            f.write(str(structs[i].constant) + "\n" + "\n")

            f.close()
    if nothing_written == 1:
        saveLabel = Label(history, text="Params have been saved",bg='#CCFFE5',fg='black')
        saveLabel.pack()
        history.after(2000,saveLabel.pack_forget)
    else:
        not_saveLabel = Label(history, text="Nothing to be saved",bg='#CCFFE5',fg='black')
        not_saveLabel.pack()
        history.after(2000,not_saveLabel.pack_forget)

    return

def SaveParams(Options):
    saveLabel = Label(Options, text="Params have been saved",bg='#CCFFE5',fg='black')
    already_saved = Label(Options, text="Params are already saved",bg='#CCFFE5',fg='black')
    
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
    filename = root.filename
    free_to_write = 0
    if not filename:
        return
    try:
        f_read = open(filename, "r")
        while True: 
            line = f_read.readline()
            if not line: 
                break
            if "DC Motor Params" in line:

                voltage_file = f_read.readline().strip()
                MOI_file = f_read.readline().strip()
                armature_resistance_file = f_read.readline().strip()
                armature_unductance_file = f_read.readline().strip()
                damping_file = f_read.readline().strip()
                constant_file = f_read.readline().strip()

                if (float(voltage_file) == float(Voltage_input.get()) and float(MOI_file) == float(MOI_input.get()) and float(armature_resistance_file) == float(armature_resistance_input.get()) and
                float(armature_unductance_file) == float(armature_unductance_input.get()) and float(damping_file) == float(damping_input.get()) and float(constant_file) == float(constant_input.get())):
                    free_to_write = 1
                    break

        f_read.close()
    except IOError:
        create_file = Label(Options, text="File is created",bg='#CCFFE5',fg='black')
        create_file.grid(pady=10)
        Options.after(2000,create_file.grid_forget)
    
    if free_to_write == 0:
        saveLabel.grid(pady=10)
        Options.after(2000,saveLabel.grid_forget)
        f = open(filename, "a+")
        
        f.write("DC Motor Params\n")

        f.write(str(Voltage_input.get()) + "\n")
        f.write(str(MOI_input.get()) + "\n")
        f.write(str(armature_resistance_input.get()) + "\n")
        f.write(str(armature_unductance_input.get()) + "\n")
        f.write(str(damping_input.get()) + "\n")
        f.write(str(constant_input.get()) + "\n" + "\n")

        f.close()
    else:
        already_saved.grid(pady=10)
        Options.after(2000,already_saved.grid_forget)
    
    return

def load_file(history):
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
    filename = root.filename
    if not filename:
        return
    try:
        f_read = open(filename, "r")
        while True: 
            line = f_read.readline()
            if not line: 
                break
            if "DC Motor Params" in line:

                voltage_file = f_read.readline().strip()
                MOI_file = f_read.readline().strip()
                armature_resistance_file = f_read.readline().strip()
                armature_unductance_file = f_read.readline().strip()
                damping_file = f_read.readline().strip()
                constant_file = f_read.readline().strip()
                if not structs:
                    structs.append(Struct(str(voltage_file),str(MOI_file),str(armature_resistance_file),str(armature_unductance_file),str(constant_file),str(damping_file)))
                else:
                    len_struct = len(structs)
                    original = 0
                    for i in range(0,len_struct):
                        if ((float(structs[i].voltage) != float(voltage_file)) or float(structs[i].moi) != float(MOI_file) or float(structs[i].resistance) != float(armature_resistance_file) or
                        float(structs[i].inductance) != float(armature_unductance_file) or float(structs[i].damping) != float(damping_file) or float(structs[i].constant) != float(constant_file)):  
                            continue
                        else:
                            original = 1
                            break
                    if original == 0:
                        structs.append(Struct(str(voltage_file),str(MOI_file),str(armature_resistance_file),str(armature_unductance_file),str(constant_file),str(damping_file)))

        history.destroy()
        ViewHistory(root)

    except IOError:
        no_file_to_read_from = Label(history, text="No such file or directory",bg='#CCFFE5',fg='black')
        no_file_to_read_from.pack()
        history.after(2000,no_file_to_read_from.pack_forget)

    return

def compare(comparison,no_config_compare):
    if (len(structs) == 0):
        hs_clear = Label(comparison, text="History is clear!",bg='#CCFFE5',fg='black')
        hs_clear.pack()
        comparison.after(2000,hs_clear.pack_forget)
    elif (len(no_config_compare.get())==0 or RepresentsInt_2(no_config_compare.get())== False or float(no_config_compare.get()) < 0):
        errno_valid_number = Label(comparison, text="Introduce a valid number!",bg='#CCFFE5',fg='black')
        errno_valid_number.pack()
        comparison.after(2000,errno_valid_number.pack_forget)
    elif (len(structs) <= float(no_config_compare.get())):
        errno = Label(comparison, text="Introduce a valid number!",bg='#CCFFE5',fg='black')
        errno.pack()
        comparison.after(2000,errno.pack_forget)
    else:
        index = int(no_config_compare.get())
        options_compare = tk.Toplevel(comparison)
        options_compare.title('Options Compare')
        options_compare.geometry("400x600")
        options_compare.configure(bg='#CCFFE5')
        if not structs:
            structs.append(Struct(str(Voltage_input.get()),str(MOI_input.get()),str(armature_resistance_input.get()),str(armature_unductance_input.get()),str(constant_input.get()),str(damping_input.get())))
        else:
            len_struct = len(structs)
            original = 0
            for i in range(0,len_struct):
                if (float(structs[i].voltage) != float(Voltage_input.get()) or float(structs[i].moi) != float(MOI_input.get()) or float(structs[i].resistance) != float(armature_resistance_input.get()) or
                float(structs[i].inductance) != float(armature_unductance_input.get()) or float(structs[i].damping) != float(damping_input.get()) or float(structs[i].constant) != float(constant_input.get())):  
                    continue
                else:
                    original = 1
                    break
            if original == 0:
                structs.append(Struct(str(Voltage_input.get()),str(MOI_input.get()),str(armature_resistance_input.get()),str(armature_unductance_input.get()),str(constant_input.get()),str(damping_input.get())))

        Button(options_compare, text="Current Intensity Plot", command=lambda: current_index(index,-1), fg="white", bg="#137ab1",bd=3).grid(row=0,padx=130,pady=10)
        Button(options_compare, text="Angular Velocity Plot", command=lambda:speed_theta(index,-1), fg="white", bg="#137ab1",bd=3).grid(row=1,padx=130,pady=10)
        Button(options_compare, text="Torque Plot", command=lambda:torque_plot(index,-1), fg="white", bg="#137ab1",bd=3).grid(row=2,padx=130,pady=10)
        Button(options_compare, text="Electromotive Force Plot", command=lambda:electromotive_force_plot(index,-1), fg="white", bg="#137ab1",bd=3).grid(row=3,padx=130,pady=10)
        Button(options_compare, text="Back", command=options_compare.destroy,fg="white", bg="#137ab1",bd=3).grid(row=5,padx=130,pady=10)

        T = tk.Text(options_compare, height=18, width=20,fg="white",bg="#165174")
        T.grid(row=6,padx=130,pady=10)
        T.insert(tk.END, "DC Motor Parameters\n")
        T.insert(tk.END, "V1 = " + str(Voltage_input.get()) + "\nV2 = " + structs[index].voltage +  "\n\n")
        T.insert(tk.END, "J1 = " + str(MOI_input.get()) + "\nJ2 = " + structs[index].moi +"\n\n")
        T.insert(tk.END, "R1 = " + str(armature_resistance_input.get()) + "\nR2 = " + structs[index].resistance + "\n\n")
        T.insert(tk.END, "L1 = " + str(armature_unductance_input.get()) + "\nL2 = " + structs[index].inductance +"\n\n")
        T.insert(tk.END, "B1 = " + str(damping_input.get()) + "\nB2 = " + structs[index].damping +"\n\n")
        T.insert(tk.END, "K1 = " + str(constant_input.get()) + "\nK2 = " + structs[index].constant)


        options_compare.transient(comparison)
        options_compare.grab_set()
        comparison.wait_window(options_compare)
    return

def compare_manual(comparison_manual,Voltage_input_manual,
    MOI_input_manual,armature_resistance_input_manual,armature_unductance_input_manual,damping_input_manual,constant_input_manual):
    global voltage_manual
    global moi_manual 
    global res_manual 
    global induc_manual
    global damping_manual
    global ct_manual
    error_manual = Label(comparison_manual, text="Not all fields were completed or some fields do not \nrepresent numbers/valid numbers!",bg='#CCFFE5',fg='black')
    error_voltage_manual = Label(comparison_manual, text="Voltage must be set!",bg='#CCFFE5',fg='black')
    if ((len(MOI_input_manual.get())==0 or RepresentsInt(MOI_input_manual.get())== False or float(MOI_input_manual.get()) <= 0) or
            (len(armature_resistance_input_manual.get())==0 or RepresentsInt(armature_resistance_input_manual.get())== False or float(armature_resistance_input_manual.get()) <= 0) or
            (len(armature_unductance_input_manual.get())==0 or RepresentsInt(armature_unductance_input_manual.get())== False or float(armature_unductance_input_manual.get()) <= 0) or
            (len(damping_input_manual.get())==0 or RepresentsInt(damping_input_manual.get())== False or float(damping_input_manual.get()) <= 0) or
            (len(constant_input_manual.get())==0) or RepresentsInt(constant_input_manual.get())== False or float(constant_input_manual.get()) <= 0): 
        error_manual.pack()
        comparison_manual.after(2000,error_manual.pack_forget)
        if (Voltage_input_manual.get() == 0):
            error_voltage_manual.pack()
            comparison_manual.after(2000,error_voltage_manual.pack_forget)
    elif (Voltage_input_manual.get() == 0):
        error_voltage_manual.pack()
        comparison_manual.after(2000,error_voltage_manual.pack_forget)
    else:
        Options_manual = tk.Toplevel(comparison_manual)
        Options_manual.title('Options manual compare')
        Options_manual.geometry("400x600")
        Options_manual.configure(bg='#CCFFE5')

        if not structs:
            structs.append(Struct(str(Voltage_input_manual.get()),str(MOI_input_manual.get()),str(armature_resistance_input_manual.get()),str(armature_unductance_input_manual.get()),str(constant_input_manual.get()),str(damping_input_manual.get())))
        else:
            len_struct = len(structs)
            original = 0
            for i in range(0,len_struct):
                if (float(structs[i].voltage) != float(Voltage_input_manual.get()) or float(structs[i].moi) != float(MOI_input_manual.get()) or float(structs[i].resistance) != float(armature_resistance_input_manual.get()) or
                float(structs[i].inductance) != float(armature_unductance_input_manual.get()) or float(structs[i].damping) != float(damping_input_manual.get()) or float(structs[i].constant) != float(constant_input_manual.get())):  
                    continue
                else:
                    original = 1
                    break
            if original == 0:
                structs.append(Struct(str(Voltage_input_manual.get()),str(MOI_input_manual.get()),str(armature_resistance_input_manual.get()),str(armature_unductance_input_manual.get()),str(constant_input_manual.get()),str(damping_input_manual.get())))

        if not structs:
            structs.append(Struct(str(Voltage_input.get()),str(MOI_input.get()),str(armature_resistance_input.get()),str(armature_unductance_input.get()),str(constant_input.get()),str(damping_input.get())))
        else:
            len_struct = len(structs)
            original = 0
            for i in range(0,len_struct):
                if (float(structs[i].voltage) != float(Voltage_input.get()) or float(structs[i].moi) != float(MOI_input.get()) or float(structs[i].resistance) != float(armature_resistance_input.get()) or
                float(structs[i].inductance) != float(armature_unductance_input.get()) or float(structs[i].damping) != float(damping_input.get()) or float(structs[i].constant) != float(constant_input.get())):  
                    continue
                else:
                    original = 1
                    break
            if original == 0:
                structs.append(Struct(str(Voltage_input.get()),str(MOI_input.get()),str(armature_resistance_input.get()),str(armature_unductance_input.get()),str(constant_input.get()),str(damping_input.get())))


        voltage_manual = float(Voltage_input_manual.get())
        moi_manual = float(MOI_input_manual.get())
        res_manual = float(armature_resistance_input_manual.get())
        induc_manual = float(armature_unductance_input_manual.get())
        damping_manual = float(damping_input_manual.get())
        ct_manual = float(constant_input_manual.get())

        Button(Options_manual, text="Current Intensity Plot", command=lambda:current_index(-1,-2), fg="white", bg="#137ab1",bd=3).grid(row=0,padx=130,pady=10)

        Button(Options_manual, text="Angular Velocity Plot", command=lambda:speed_theta(-1,-2), fg="white", bg="#137ab1",bd=3).grid(row=1,padx=130,pady=10)

        Button(Options_manual, text="Torque Plot", command=lambda:torque_plot(-1,-2), fg="white", bg="#137ab1",bd=3).grid(row=2,padx=130,pady=10)

        Button(Options_manual, text="Electromotive Force Plot", command=lambda:electromotive_force_plot(-1,-2), fg="white", bg="#137ab1",bd=3).grid(row=3,padx=130,pady=10)

        Button(Options_manual, text="Back", command=Options_manual.destroy,fg="white", bg="#137ab1",bd=3).grid(row=5,padx=130,pady=10)

        T = tk.Text(Options_manual, height=18, width=20,fg="white",bg="#165174")
        T.grid(row=6,padx=130,pady=10)
        T.insert(tk.END, "DC Motor Parameters\n")
        T.insert(tk.END, "V1 = " + str(Voltage_input.get()) + "\nV2 = " + str(voltage_manual) +  "\n\n")
        T.insert(tk.END, "J1 = " + str(MOI_input.get()) + "\nJ2 = " + str(moi_manual) +"\n\n")
        T.insert(tk.END, "R1 = " + str(armature_resistance_input.get()) + "\nR2 = " + str(res_manual) + "\n\n")
        T.insert(tk.END, "L1 = " + str(armature_unductance_input.get()) + "\nL2 = " + str(induc_manual) +"\n\n")
        T.insert(tk.END, "B1 = " + str(damping_input.get()) + "\nB2 = " + str(damping_manual) +"\n\n")
        T.insert(tk.END, "K1 = " + str(constant_input.get()) + "\nK2 = " + str(ct_manual))

        Options_manual.transient(comparison_manual)
        Options_manual.grab_set()
        comparison_manual.wait_window(Options_manual)


    return

def manualCompare(comparison):
    comparison_manual = tk.Toplevel(comparison)
    comparison_manual.title('Manual Comparison')
    comparison_manual.geometry("400x600")
    comparison_manual.configure(bg='#CCFFE5')



    Voltage_text_manual = Label(comparison_manual, text="Enter voltage(V):",bg='#CCFFE5',fg="black")
    Voltage_text_manual.pack()

    Voltage_input_manual = Scale(comparison_manual, from_=0, to=20,orient=HORIZONTAL,fg="white", bg="#137ab1",bd=10,resolution=-1,relief=RIDGE,highlightthickness=0,troughcolor = '#CCFFE5')
    Voltage_input_manual.pack()


    #momentul de inertie
    MOI_text_manual = Label(comparison_manual, text="Enter moment of inertia(J - kg*m^2):",bg='#CCFFE5',fg="black")
    MOI_text_manual.pack()


    MOI_input_manual = Entry(comparison_manual,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
    MOI_input_manual.pack()

    armature_resistance_text_manual = Label(comparison_manual, text="Enter armature resistance(R - Ω):",bg='#CCFFE5',fg="black")
    armature_resistance_text_manual.pack()

    armature_resistance_input_manual = Entry(comparison_manual,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
    armature_resistance_input_manual.pack()

    armature_unductance_text_manual = Label(comparison_manual, text="Enter armature inductance(L - H):",bg='#CCFFE5',fg="black")
    armature_unductance_text_manual.pack()

    armature_unductance_input_manual = Entry(comparison_manual,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
    armature_unductance_input_manual.pack()

    damping_text_manual = Label(comparison_manual, text="Enter damping(B - N*m*s):",bg='#CCFFE5',fg="black")
    damping_text_manual.pack()

    damping_input_manual = Entry(comparison_manual,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
    damping_input_manual.pack()

    constant_text_manual = Label(comparison_manual, text="Enter constant(K - N*m/A):",bg='#CCFFE5',fg="black")
    constant_text_manual.pack()

    constant_input_manual = Entry(comparison_manual,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
    constant_input_manual.pack()

    compare_button_manual = Button(comparison_manual, text="Compare", command=lambda: compare_manual(comparison_manual,Voltage_input_manual,
    MOI_input_manual,armature_resistance_input_manual,armature_unductance_input_manual,damping_input_manual,constant_input_manual), fg="white", bg="#137ab1",bd=3)
    compare_button_manual.pack(pady=20)

    Button(comparison_manual, text="Back", command=comparison_manual.destroy,fg="white", bg="#137ab1",bd=3).pack(pady=20)



    comparison_manual.transient(comparison)
    comparison_manual.grab_set()
    comparison.wait_window(comparison_manual)

    return
def compareTo(root):
    if ((len(N_input.get())==0 or RepresentsInt(N_input.get())== False or float(N_input.get()) <= 0 or float(N_input.get()) > 100) or
            (len(MOI_input.get())==0 or RepresentsInt(MOI_input.get())== False or float(MOI_input.get()) <= 0) or
            (len(armature_resistance_input.get())==0 or RepresentsInt(armature_resistance_input.get())== False  or float(armature_resistance_input.get()) <= 0) or
            (len(armature_unductance_input.get())==0 or RepresentsInt(armature_unductance_input.get())== False or float(armature_unductance_input.get()) <= 0) or
            (len(damping_input.get())==0 or RepresentsInt(damping_input.get())== False or float(damping_input.get()) <= 0) or
            (len(constant_input.get())==0) or RepresentsInt(constant_input.get())== False or float(constant_input.get()) <= 0):
        error.pack()
        root.after(2000,error.pack_forget)
        if (Voltage_input.get() == 0):
            error_voltage.pack()
            root.after(2000,error_voltage.pack_forget)
    elif (Voltage_input.get() == 0):
        error_voltage.pack()
        root.after(2000,error_voltage.pack_forget)
    else:
        comparison = tk.Toplevel(root)
        comparison.title('Compare')
        comparison.geometry("400x600")
        comparison.configure(bg='#CCFFE5')


        scrollbar = Scrollbar(comparison)
        scrollbar.pack( side = RIGHT, fill = Y )
        mylist = Listbox(comparison, yscrollcommand = scrollbar.set ,bg="#165174",fg = "white",width = 35)
        Label(comparison, text="Enter number of configuration to compare with",bg='#CCFFE5',fg="black").pack()
        no_config_compare = Entry(comparison,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
        no_config_compare.pack()

        compare_button = Button(comparison, text="Compare", command=lambda: compare(comparison,no_config_compare), fg="white", bg="#137ab1",bd=3)
        compare_button.pack()

        Label(comparison, text="or",bg='#CCFFE5',fg="black").pack()

        compare_button_manual = Button(comparison, text="Manual comparison", command=lambda: manualCompare(comparison), fg="white", bg="#137ab1",bd=3)
        compare_button_manual.pack()

        back_manual = Button(comparison, text="Back", command=comparison.destroy, fg="white", bg="#137ab1",bd=3)
        back_manual.pack(pady=10)

        for i in range(0,len(structs)):
            mylist.insert(tk.END, "DC Motor Parameters " + "No. " + str(i) + "\n")
            mylist.insert(tk.END, "V = " + structs[i].voltage + "\n")
            mylist.insert(tk.END, "J = " + structs[i].moi + "\n")
            mylist.insert(tk.END, "R = " + structs[i].resistance + "\n")
            mylist.insert(tk.END, "L = " + structs[i].inductance + "\n")
            mylist.insert(tk.END, "B = " + structs[i].damping + "\n")
            mylist.insert(tk.END, "K = " + structs[i].constant + "\n")
            mylist.insert(tk.END,"\n")
        mylist.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = mylist.yview )

        comparison.transient(root)
        comparison.grab_set()
        root.wait_window(comparison)
    
    return


def compare_two(history,first_compare,second_compare):
    valid_entry = 0
    if (len(N_input.get())==0 or RepresentsInt(N_input.get())== False or float(N_input.get()) <= 0):
        error_no_seconds_set = Label(history, text="No time/valid time has been set!",bg='#CCFFE5',fg='black')
        error_no_seconds_set.pack()
        history.after(2000,error_no_seconds_set.pack_forget)
        valid_entry = 1
    if (len(first_compare.get())==0  or len(second_compare.get())==0 ):
        complete_fields = Label(history, text="Complete suggested fields(*)!",bg='#CCFFE5',fg='black')
        complete_fields.pack()
        history.after(2000,complete_fields.pack_forget)
        valid_entry = 1
    elif (len(structs) <= float(first_compare.get()) or len(structs) <= float(second_compare.get()) or float(second_compare.get()) < 0 or float(first_compare.get()) < 0
    or RepresentsInt_2(first_compare.get())== False or RepresentsInt_2(second_compare.get()) == False):
        invalid_index = Label(history, text="Invalid index!",bg='#CCFFE5',fg='black')
        invalid_index.pack()
        history.after(2000,invalid_index.pack_forget)
        valid_entry = 1
    if valid_entry == 0:
        index1 = int(first_compare.get())
        index2 = int(second_compare.get())

        options_compare_two = tk.Toplevel(history)
        options_compare_two.title('Options Compare')
        options_compare_two.geometry("400x600")
        options_compare_two.configure(bg='#CCFFE5')
        
        Button(options_compare_two, text="Current Intensity Plot", command=lambda: current_index(index1,index2), fg="white", bg="#137ab1",bd=3).grid(row=0,padx=130,pady=10)
        Button(options_compare_two, text="Angular Velocity Plot", command=lambda:speed_theta(index1,index2), fg="white", bg="#137ab1",bd=3).grid(row=1,padx=130,pady=10)
        Button(options_compare_two, text="Torque Plot", command=lambda:torque_plot(index1,index2), fg="white", bg="#137ab1",bd=3).grid(row=2,padx=130,pady=10)
        Button(options_compare_two, text="Electromotive Force Plot", command=lambda:electromotive_force_plot(index1,index2), fg="white", bg="#137ab1",bd=3).grid(row=3,padx=130,pady=10)
        Button(options_compare_two, text="Back", command=options_compare_two.destroy,fg="white", bg="#137ab1",bd=3).grid(row=5,padx=130,pady=10)

        T = tk.Text(options_compare_two, height=18, width=20,fg="white",bg="#165174")
        T.grid(row=6,padx=130,pady=10)
        T.insert(tk.END, "DC Motor Parameters\n")
        T.insert(tk.END, "V1 = " + structs[index1].voltage + "\nV2 = " + structs[index2].voltage +  "\n\n")
        T.insert(tk.END, "J1 = " + structs[index1].moi + "\nJ2 = " + structs[index2].moi +"\n\n")
        T.insert(tk.END, "R1 = " + structs[index1].resistance + "\nR2 = " + structs[index2].resistance + "\n\n")
        T.insert(tk.END, "L1 = " + structs[index1].inductance + "\nL2 = " + structs[index2].inductance +"\n\n")
        T.insert(tk.END, "B1 = " + structs[index1].damping + "\nB2 = " + structs[index2].damping +"\n\n")
        T.insert(tk.END, "K1 = " + structs[index1].constant + "\nK2 = " + structs[index2].constant)


        options_compare_two.transient(history)
        options_compare_two.grab_set()
        history.wait_window(options_compare_two)
    return
def ViewHistory(root):
    history = tk.Toplevel(root)
    history.title('History')
    history.geometry("400x600")
    history.configure(bg='#CCFFE5')


    scrollbar = Scrollbar(history)
    scrollbar.pack( side = RIGHT, fill = Y )
    mylist = Listbox(history, yscrollcommand = scrollbar.set ,bg="#165174",fg = "white",width = 35)

    Label(history, text="Enter number of configuration",bg='#CCFFE5',fg="black").pack()

    no_config = Entry(history,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
    no_config.pack()

    b = Button(history, text="Load", command=lambda: load(history,no_config), fg="white", bg="#137ab1",bd=3)
    b.pack()

    Button(history, text="Load from file", command=lambda: load_file(history), fg="white", bg="#137ab1",bd=3).pack()
    Button(history, text="Save to file", command=lambda: save_file(history), fg="white", bg="#137ab1",bd=3).pack()

    first_compare = Entry(history,width=20,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
    second_compare = Entry(history,width=20,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")


    first_compare.insert(0,'Enter configuration (*)')
    first_compare.pack(pady=5)

    def on_clickcmp1(event):
        first_compare.configure(state=NORMAL)
        first_compare.delete(0, END)
        first_compare.unbind('<Button-1>', on_click_idcmp1)
    on_click_idcmp1 = first_compare.bind('<Button-1>', on_clickcmp1)

    second_compare.insert(0,'Enter configuration (*)')
    second_compare.pack()

    def on_clickcmp2(event):
        second_compare.configure(state=NORMAL)
        second_compare.delete(0, END)
        second_compare.unbind('<Button-1>', on_click_idcmp2)
    on_click_idcmp2 = second_compare.bind('<Button-1>', on_clickcmp2)

    Button(history, text="Compare", command=lambda: compare_two(history,first_compare,second_compare), fg="white", bg="#137ab1",bd=3).pack(pady=5)
    Button(history, text="Back", command=history.destroy, fg="white", bg="#137ab1",bd=3).pack(pady=5)


    for i in range(0,len(structs)):
        mylist.insert(tk.END, "DC Motor Parameters " + "No. " + str(i) + "\n")
        mylist.insert(tk.END, "V = " + structs[i].voltage + "\n")
        mylist.insert(tk.END, "J = " + structs[i].moi + "\n")
        mylist.insert(tk.END, "R = " + structs[i].resistance + "\n")
        mylist.insert(tk.END, "L = " + structs[i].inductance + "\n")
        mylist.insert(tk.END, "B = " + structs[i].damping + "\n")
        mylist.insert(tk.END, "K = " + structs[i].constant + "\n")
        mylist.insert(tk.END,"\n")
    mylist.pack( side = LEFT, fill = BOTH )
    scrollbar.config( command = mylist.yview )
    history.transient(root)
    history.grab_set()
    root.wait_window(history)
    return

def set(object,float):
    object.delete(0,"end")
    object.insert(0, float)

def load(history,no_config):
    if (len(structs) == 0):
        hs_clear = Label(history, text="History is clear!",bg='#CCFFE5',fg="black")
        hs_clear.pack()
        history.after(2000,hs_clear.destroy)
        return
    if (len(no_config.get())==0 or RepresentsInt_2(no_config.get())== False):
        valid_number = Label(history, text="Introduce a valid number!",bg='#CCFFE5',fg="black")
        valid_number.pack()
        history.after(2000,valid_number.destroy)
    elif (len(structs) <= float(no_config.get()) or float(no_config.get()) < 0):
        valid_number = Label(history, text="Introduce a valid number!",bg='#CCFFE5',fg="black")
        valid_number.pack()
        history.after(2000,valid_number.destroy)
    else:
        Voltage_input.set(structs[int(no_config.get())].voltage)
        set(MOI_input,structs[int(no_config.get())].moi)
        set(armature_resistance_input,structs[int(no_config.get())].resistance)
        set(armature_unductance_input,structs[int(no_config.get())].inductance)
        set(damping_input,structs[int(no_config.get())].damping)
        set(constant_input,structs[int(no_config.get())].constant)
        history.destroy()

cam = Camera()
WIDTH, HEIGHT = 1080, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False



def animation():
    def key_input_clb(window, key, scancode, action, mode):
        global left, right, forward, backward


        if key == glfw.KEY_W and action == glfw.PRESS:
            forward = True
        elif key == glfw.KEY_W and action == glfw.RELEASE:
            forward = False
        if key == glfw.KEY_S and action == glfw.PRESS:
            backward = True
        elif key == glfw.KEY_S and action == glfw.RELEASE:
            backward = False
        if key == glfw.KEY_A and action == glfw.PRESS:
            left = True
        elif key == glfw.KEY_A and action == glfw.RELEASE:
            left = False
        if key == glfw.KEY_D and action == glfw.PRESS:
            right = True
        elif key == glfw.KEY_D and action == glfw.RELEASE:
            right = False

    def do_movement():
        if left:
            cam.process_keyboard("LEFT", 0.02)
        if right:
            cam.process_keyboard("RIGHT", 0.02)
        if forward:
            cam.process_keyboard("FORWARD", 0.02)
        if backward:
            cam.process_keyboard("BACKWARD", 0.02)


    global current_time
    global pas
    N = int(N_input.get()) * 100
    global curr_index
    global w_vector


    curr_index = 0
    w_vector = [0] * N
    pas = 0.01
    for i in range(0, N):
        calculate_index(-1)

    
    i = 0
    count = 0


    vertex_src = """
    # version 330
    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec2 a_texture;
    layout(location = 2) in vec3 a_normal;
    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;
    out vec2 v_texture;
    void main()
    {
        gl_Position = projection * view * model * vec4(a_position, 1.0);
        v_texture = a_texture;
    }
    """

    fragment_src = """
    # version 330
    in vec2 v_texture;
    out vec4 out_color;
    uniform sampler2D s_texture;
    void main()
    {
        out_color = texture(s_texture, v_texture);
    }
    """


    def window_resize_clb(window, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(90, 1080 / 720, 0.1, 100)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    if not glfw.init():
        raise Exception("glfw can not be initialized!")

    window = glfw.create_window(1080, 720, "DC Motor Animation", None, None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    glfw.set_window_size_callback(window, window_resize_clb)
    glfw.set_key_callback(window, key_input_clb)
    glfw.make_context_current(window)

    chibi_indices, chibi_buffer = ObjLoader.load_model("meshes/cubes.obj")
    monkey_indices, monkey_buffer = ObjLoader.load_model("meshes/corners.obj")
    plus_indices, plus_buffer = ObjLoader.load_model("meshes/plus.obj")
    minus_indices, minus_buffer = ObjLoader.load_model("meshes/minus.obj")
    armature_indices, armature_buffer = ObjLoader.load_model("meshes/armature.obj")
    quads_indices, quads_buffer = ObjLoader.load_model("meshes/quads.obj")

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    VAO = glGenVertexArrays(6)
    VBO = glGenBuffers(6)

    glBindVertexArray(VAO[0])

    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, chibi_buffer.nbytes, chibi_buffer, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(12))

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    glBindVertexArray(VAO[1])

    glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
    glBufferData(GL_ARRAY_BUFFER, monkey_buffer.nbytes, monkey_buffer, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(12))

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    glBindVertexArray(VAO[2])

    glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
    glBufferData(GL_ARRAY_BUFFER, plus_buffer.nbytes, plus_buffer, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, plus_buffer.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, plus_buffer.itemsize * 8, ctypes.c_void_p(12))

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, plus_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    glBindVertexArray(VAO[3])

    glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
    glBufferData(GL_ARRAY_BUFFER, armature_buffer.nbytes, armature_buffer, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, armature_buffer.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, armature_buffer.itemsize * 8, ctypes.c_void_p(12))

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, armature_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    glBindVertexArray(VAO[4])

    glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
    glBufferData(GL_ARRAY_BUFFER, minus_buffer.nbytes, minus_buffer, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, minus_buffer.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, minus_buffer.itemsize * 8, ctypes.c_void_p(12))

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, minus_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)


    glBindVertexArray(VAO[5])

    glBindBuffer(GL_ARRAY_BUFFER, VBO[5])
    glBufferData(GL_ARRAY_BUFFER, quads_buffer.nbytes, quads_buffer, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, quads_buffer.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, quads_buffer.itemsize * 8, ctypes.c_void_p(12))

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, quads_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)


    textures = glGenTextures(6)
    load_texture("Pictures/DC.png", textures[0])
    load_texture("Pictures/wire.png", textures[1])
    load_texture("Pictures/battery.png", textures[2])
    load_texture("Pictures/armature.png", textures[3])
    load_texture("Pictures/minus.png", textures[4])
    load_texture("Pictures/armature.png", textures[5])

    glUseProgram(shader)
    glClearColor(204/255, 1.0, 229/255, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    projection = pyrr.matrix44.create_perspective_projection_matrix(90.0, 1080 / 720, 0.1, 100.0)
    chibi_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -4, -15]))
    monkey_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -4, -15]))
    plus_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -4, -15]))
    minus_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -4, -15]))
    armature_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -4, -15]))
    quads_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -4, -15]))

    model_loc = glGetUniformLocation(shader, "model")
    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        rot_y = pyrr.Matrix44.from_y_rotation(0)
        model = pyrr.matrix44.multiply(rot_y, chibi_pos)

        glBindVertexArray(VAO[0])
        glBindTexture(GL_TEXTURE_2D, textures[0])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(chibi_indices))

        model = pyrr.matrix44.multiply(rot_y, monkey_pos)

        glBindVertexArray(VAO[1])
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(monkey_indices))


        model = pyrr.matrix44.multiply(rot_y, plus_pos)

        glBindVertexArray(VAO[2])
        glBindTexture(GL_TEXTURE_2D, textures[2])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(plus_indices))

        model = pyrr.matrix44.multiply(rot_y, minus_pos)

        glBindVertexArray(VAO[4])
        glBindTexture(GL_TEXTURE_2D, textures[4])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(minus_indices))

        model = pyrr.matrix44.multiply(rot_y, quads_pos)

        glBindVertexArray(VAO[5])
        glBindTexture(GL_TEXTURE_2D, textures[5])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(quads_indices))


        rot = 0.5
        rot_z = pyrr.Matrix44.from_z_rotation(-w_vector[i] * rot * glfw.get_time())
        count += 1
        if count % 50 == 0:
            i = i + 1
        if i == N:
            i -= 1
        model = pyrr.matrix44.multiply(rot_z, armature_pos)

        glBindVertexArray(VAO[3])
        glBindTexture(GL_TEXTURE_2D, textures[3])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(armature_indices))

        glfw.swap_buffers(window)

    glfw.terminate()

    return
def options():
    if (len(N_input.get())!=0 and int(N_input.get()) > 100):
        N_seconds = Label(root, text="Motor can be active maximum 100 seconds",bg='#CCFFE5',fg='black')
        N_seconds.pack()
        root.after(2000,N_seconds.pack_forget)
        return
    if ((len(N_input.get())==0 or RepresentsInt(N_input.get())== False or float(N_input.get()) <= 0) or
            (len(MOI_input.get())==0 or RepresentsInt(MOI_input.get())== False or float(MOI_input.get()) <= 0) or
            (len(armature_resistance_input.get())==0 or RepresentsInt(armature_resistance_input.get())== False  or float(armature_resistance_input.get()) <= 0) or
            (len(armature_unductance_input.get())==0 or RepresentsInt(armature_unductance_input.get())== False or float(armature_unductance_input.get()) <= 0) or
            (len(damping_input.get())==0 or RepresentsInt(damping_input.get())== False or float(damping_input.get()) <= 0) or
            (len(constant_input.get())==0) or RepresentsInt(constant_input.get())== False or float(constant_input.get()) <= 0):
        error.pack()
        if (Voltage_input.get() == 0):
            error_voltage.pack()
            root.after(2000,error_voltage.pack_forget)
        root.after(2000,error.pack_forget)
    elif (Voltage_input.get() == 0):
        error_voltage.pack()
        root.after(2000,error_voltage.pack_forget)
    else:
        Options = tk.Toplevel(root)
        Options.title('Options')
        Options.geometry("400x600")
        Options.configure(bg='#CCFFE5')
        if not structs:
            structs.append(Struct(str(Voltage_input.get()),str(MOI_input.get()),str(armature_resistance_input.get()),str(armature_unductance_input.get()),str(constant_input.get()),str(damping_input.get())))
        else:
            len_struct = len(structs)
            original = 0
            for i in range(0,len_struct):
                if (float(structs[i].voltage) != float(Voltage_input.get()) or float(structs[i].moi) != float(MOI_input.get()) or float(structs[i].resistance) != float(armature_resistance_input.get()) or
                float(structs[i].inductance) != float(armature_unductance_input.get()) or float(structs[i].damping) != float(damping_input.get()) or float(structs[i].constant) != float(constant_input.get())):  
                    continue
                else:
                    original = 1
                    break
            if original == 0:
                structs.append(Struct(str(Voltage_input.get()),str(MOI_input.get()),str(armature_resistance_input.get()),str(armature_unductance_input.get()),str(constant_input.get()),str(damping_input.get())))
        
        Button(Options, text="Current Intensity Plot", command=lambda:current_index(-1,-1), fg="white", bg="#137ab1",bd=3).grid(row=0,padx=130,pady=10)
        Button(Options, text="Angular Velocity Plot", command=lambda:speed_theta(-1,-1), fg="white", bg="#137ab1",bd=3).grid(row=1,padx=130,pady=10)
        Button(Options, text="Torque Plot", command=lambda:torque_plot(-1,-1), fg="white", bg="#137ab1",bd=3).grid(row=2,padx=130,pady=10)
        Button(Options, text="Electromotive Force Plot", command=lambda:electromotive_force_plot(-1,-1), fg="white", bg="#137ab1",bd=3).grid(row=3,padx=130,pady=10)
        Button(Options, text="Animation", command=animation,fg="white", bg="#137ab1",bd=3).grid(row=4,padx=130,pady=10)
        Button(Options, text="Back", command=Options.destroy,fg="white", bg="#137ab1",bd=3).grid(row=5,padx=130,pady=10)

        T = tk.Text(Options, height=7, width=20,fg="white",bg="#165174")
        T.grid(row=6,padx=130,pady=10)
        T.insert(tk.END, "DC Motor Parameters\n")
        T.insert(tk.END, "V = " + str(Voltage_input.get()) + "\n")
        T.insert(tk.END, "J = " + str(MOI_input.get()) + "\n")
        T.insert(tk.END, "R = " + str(armature_resistance_input.get()) + "\n")
        T.insert(tk.END, "L = " + str(armature_unductance_input.get()) + "\n")
        T.insert(tk.END, "B = " + str(damping_input.get()) + "\n")
        T.insert(tk.END, "K = " + str(constant_input.get()))

        Button(Options, text="Save", command=lambda: SaveParams(Options),fg="white", bg="#137ab1",bd=3).grid(row=7,padx=130,pady=10)


        Options.transient(root)
        Options.grab_set()
        root.wait_window(Options)
        
N_input_text = Label(root, text="Enter number of seconds to run the engine(sec):",bg='#CCFFE5',fg="black")
N_input_text.pack()

N_input = Entry(root,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
N_input.pack()

Voltage_text = Label(root, text="Enter voltage(V):",bg='#CCFFE5',fg="black")
Voltage_text.pack()

Voltage_input = Scale(root, from_=0, to=20,orient=HORIZONTAL,fg="white", bg="#137ab1",bd=10,resolution=-1,relief=RIDGE,highlightthickness=0,troughcolor = '#CCFFE5')
Voltage_input.pack()

MOI_text = Label(root, text="Enter moment of inertia(J - kg*m^2):",bg='#CCFFE5',fg="black")
MOI_text.pack()

MOI_input = Entry(root,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
MOI_input.pack()

armature_resistance_text = Label(root, text="Enter armature resistance(R - Ω):",bg='#CCFFE5',fg="black")
armature_resistance_text.pack()

armature_resistance_input = Entry(root,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
armature_resistance_input.pack()

armature_unductance_text = Label(root, text="Enter armature inductance(L - H):",bg='#CCFFE5',fg="black")
armature_unductance_text.pack()

armature_unductance_input = Entry(root,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
armature_unductance_input.pack()

damping_text = Label(root, text="Enter damping(B - N*m*s):",bg='#CCFFE5',fg="black")
damping_text.pack()

damping_input = Entry(root,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
damping_input.pack()

constant_text = Label(root, text="Enter constant(K - N*m/A):",bg='#CCFFE5',fg="black")
constant_text.pack()

constant_input = Entry(root,width=30,fg="white", bg="#165174",bd=3,insertbackground='white',cursor = "arrow")
constant_input.pack()

Button(root, text="Options", command=options,fg="white", bg="#137ab1",bd=3,width=10).pack()
Button(root, text="History", command=lambda: ViewHistory(root),fg="white", bg="#137ab1",bd=3,width=10).pack()
Button(root, text="Compare", command=lambda: compareTo(root),fg="white", bg="#137ab1",bd=3,width=10).pack()

def close():
    sys.exit()

Button(root, text="Quit", command=close,fg="white", bg="#137ab1",bd=3,width=10).pack()

width = 100
height = 50
img = Image.open("Pictures/DC_P.png")
img = img.resize((width,height), Image.ANTIALIAS)

image = ImageTk.PhotoImage(img)
image_label = Label(root,image=image)
image_label.pack(side=BOTTOM)
root.mainloop()
