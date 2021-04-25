import pickle
import datetime
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
import webbrowser
from tkcalendar import DateEntry

#Home Page
master = Tk()

# set name
appName = "Appname"

# if time to expand on symptoms later - would be challenging to iterate through these in for-loops to create buttons in tkinter so would likely have to be hardcoded
symptoms = ["Shortness of Breath", "Cough", "Fatigue", "Chest Pain", "Loss of Smell/Taste", "Brain Fog", "Low in Mood"]

labelText = "Welcome to " + appName
master.title (appName)
master.geometry ('300x300')
line1 = Label(master,text=labelText, font=('Calibri', 20))
line1.grid (column=0, row=0)

line2 = Label(master,text='We will be here through every step of your recovery', font=('Calibri', 10))
line2.grid (column=0, row=1)

# data savename
fileName = "testdata.data"

#if os.path.isfile(fileName):
#    dataExists = True
#    openFile = open(fileName, 'rb')
#    dataset = pickle.load(openFile)
#else:
#    dataExists = False
#print(dataset)

#close button function
def close():
    swindow.destroy()

#Symptom tracking
def clickedSymptom():
    swindow = Tk()
    swindow.title ("Symptom Tracking")
    swindow.geometry ('300x300')
    
    #calendar    
    def get_value():
        print(cal.get_date())
 
    choosedate = Label(swindow, text='Choose date').grid(column=0, row=0)

    cal = DateEntry(swindow, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
    cal.grid(column=0, row=1)
    
    
    # data recording and window closing functions
    def recordData():
        # record individual symptoms by clicking record symptoms button

        # pickle used locally within this function due to limitations with return statements with tkinter buttons

        
        obtainedData = [[cal.get_date()], [scaleSOB.get()], [scaleCough.get()], [scaleFatigue.get()], [scaleMood.get()]]
        #obtainedData = [[datetime.date.today()], tempData]

        # load existing data if poss
        if os.path.isfile(fileName):
            openFile = open(fileName, 'rb')
            data = pickle.load(openFile)
            data = np.append(data, obtainedData, axis=1)
        else:
            data = np.array(obtainedData)

        # save data
        savedFile = open(fileName, 'wb')
        pickle.dump(data, savedFile)
        savedFile.close()
        
    def close():
        swindow.destroy()
    
    # sliders
    varSOB = IntVar()
    #scaleSOB = Scale(swindow, orient='horizontal', from_=1, to=10, variable=varSOB, command=sliderStore(0,tempData,varSOB.get()))
    scaleSOB = Scale(swindow, orient='horizontal', from_=1, to=10, variable=varSOB)
    scaleSOB.grid(column=1, row=2)
    
    varCough = IntVar()
    scaleCough = Scale(swindow, orient='horizontal', from_=1, to=10, variable=varCough)
    scaleCough.grid(column=1, row=3)

    varFatigue = IntVar()
    scaleFatigue = Scale(swindow, orient='horizontal', from_=1, to=10, variable=varFatigue)
    scaleFatigue.grid(column=1, row=4)
    
    varMood = IntVar()
    scaleMood = Scale(swindow, orient='horizontal', from_=1, to=10, variable=varMood)
    scaleMood.grid(column=1, row=5)
    
    # text corresponding to sliders
    textSOB = Label(swindow,text="Shortness of breath", font=('Calibri', 12))
    textSOB.grid(column=0, row=2)
    
    textCough = Label(swindow,text="Cough", font=('Calibri', 12))
    textCough.grid(column=0, row=3)
    
    textFatigue = Label(swindow,text="Fatigue", font=('Calibri', 12))
    textFatigue.grid(column=0, row=4)
    
    textMood = Label(swindow,text="Mood", font=('Calibri', 12))
    textMood.grid(column=0, row=5)
    
    # recording button
    btnRec = Button(swindow, text="Save", font=('Calibri', 16), command=recordData)
    btnRec.grid(column=0,row=6)
    
    # close button
    btnClose = Button(swindow, text="Close", font=('Calibri', 16), command=close)
    btnClose.grid(column=1,row=6)

#First Button: Track Your Symptoms
btna = Button(master, text="Track Your Symptoms", bg="teal", fg="yellow", command = clickedSymptom)
btna.grid (column=0, row=3)

def clickedGraph():
    graphwindow = Tk()
    graphwindow.title ("Graphs")
    graphwindow.geometry ('600x600')
    
    # load existing data if poss
    if os.path.isfile(fileName):
        openFile = open(fileName, 'rb')
        data = pickle.load(openFile)

    def plot():
        # the figure that will contain the plot
        fig = Figure(figsize = (6, 6), dpi = 100)
        
        
        
        plotx =  fig.add_subplot(111)
        plotx.plot(data[0],data[1])

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

    # the main Tkinter window
    window = Tk()
    window.title('Plotting in Tkinter')

    # dimensions of the main window
    window.geometry("500x500")

    # button that displays the plot
    plot_button = Button(master = window, 
                         command = plot,
                         height = 2, 
                         width = 10,
                         text = "Plot")

    plot_button.pack()

    # EXAMPLE FOR DROP DOWN MENU
    # Change the label text
    def show():
        label.config( text = clicked.get() )

    # Menu options
    options = [
        "Shortness of Breath",
        "Cough",
        "Fatigue",
        "Low in Mood",
    ]

    # datatype of menu text
    clicked = StringVar()

    # initial menu text
    clicked.set( "Shortness of Breath" )

    # Create Dropdown menu
    drop = OptionMenu( graphwindow , clicked , *options )
    drop.pack()

    # Create button, it will change label text
    button = Button( graphwindow , text = "click Me" , command = show ).pack()

    # Create Label
    label = Label( graphwindow , text = " " )
    label.pack()

#Second Button: Graph Your Symptoms
btnb = Button(master, text="Graph Your Symptoms", bg="teal", fg="yellow", command = clickedGraph)
btnb.grid (column=0, row=4)

#Support Page
def clickedSupport ():
    supwindow = Tk()
    supwindow.title ("Support Page")
    supwindow.geometry ('600x600')
    supportText = """
    Every COVID patient goes through their own individual recovery process. In some cases this process is unfortunately prolonged. Our application can help you keep track of your symptoms. See links below for more information.
    """
    #textSup = Label(supwindow,text=supportText, font=('Calibri', 8))
    #textSup.grid(column=0, row=0)
    
    textbox = Text(supwindow, wrap=WORD, font=('Calibri', 10))
    
    htmlName = "Website.html"

    #textbox.tag_configure("center", justify="center")

    textbox.grid(column=0, row=0)

    textbox.insert('1.0', supportText)
    
    def closeSupport():
        supwindow.destroy()
    
    def callback(url):
        webbrowser.open_new_tab(url)

    link1 = Label(supwindow, text="NHS: Long-term Effects of COVID", fg="blue", cursor="hand2")
    link1.grid(column=0, row=1)
    link1.bind("<Button-1>", lambda e: callback("https://www.nhs.uk/conditions/coronavirus-covid-19/long-term-effects-of-coronavirus-long-covid/"))

    link2 = Label(supwindow, text="NHS: Your COVID Recovery", fg="blue", cursor="hand2")
    link2.grid(column=0, row=2)
    link2.bind("<Button-1>", lambda e: callback("https://www.yourcovidrecovery.nhs.uk/"))
    
    link3 = Label(supwindow, text="NHS: Post-COVID Syndrome (Long COVID)", fg="blue", cursor="hand2")
    link3.grid(column=0, row=3)
    link3.bind("<Button-1>", lambda e: callback("https://www.england.nhs.uk/coronavirus/post-covid-syndrome-long-covid/"))

    link4 = Label(supwindow, text="So Long COVID Support Website", fg="blue", cursor="hand2")
    link4.grid(column=0, row=4)
    link4.bind("<Button-1>", lambda e: callback("file://" + os.path.realpath(htmlName)))
    
    # close button
    btnCloseSupport = Button(supwindow, text="Close", font=('Calibri', 16), command=closeSupport)
    btnCloseSupport.grid(column=0,row=5)

#Third Button Support Page
btnc = Button(master, text="Support Page", bg="teal", fg="yellow", command = clickedSupport)
btnc.grid (column=0, row=5)

def masterExit():
    master.destroy()

#Exit Button
btnc = Button(master, text="Exit", bg="teal", fg="yellow", command = masterExit)
btnc.grid (column=0, row=7)

master.mainloop()
