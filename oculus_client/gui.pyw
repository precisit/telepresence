# import the necessary packages
from Tkinter import *
import subprocess
import time

root = Tk()

# Get screen resolution
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
# default IP
ipmain = "10.0.1.35" 
# Set top bar attributes
background_image=PhotoImage(file= "~/Dropbox/Projekt_inbyggda/precisit2.gif")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
root.title("Telepresence")
root.tk_setPalette(background='#FFFFFF')
root.geometry('%dx%d+%d+%d' % (screenWidth, 64, 0, 0))
root.overrideredirect(1)                                                        # Removing borders
root.lift()
root.wm_attributes("-topmost", True)

# Set background window
background = Tk()
background.geometry('%dx%d+%d+%d' % (screenWidth, screenHeight, 0, 64))
background.overrideredirect(1)                                                      # Removing borders
background.tk_setPalette(background='#000000')

#Uncomment to insert HUD

# Set HUD attributes
#hudText = "HUD"

#leftHUD = Tk()
#leftHUD.geometry('%dx%d+%d+%d' % (200, 100, 400, 500))
#leftHUD.overrideredirect(1)                                                      # Removing borders
#leftHUD.lift()
#leftHUD.wm_attributes("-topmost", True)
#leftHUD.attributes("-alpha", 1)                                                # Making the HUD windown transparent 

#lefttext = Text(leftHUD, height=2, width=30, font = ('Comic Sans', 30, 'bold'))
#lefttext.pack()
#lefttext.insert(END, hudText)

#rightHUD = Tk()
#rightHUD.geometry('%dx%d+%d+%d' % (200, 100, 1300, 500))
#rightHUD.overrideredirect(1)                                                      # Removing borders
#rightHUD.lift()
#rightHUD.wm_attributes("-topmost", True)
#rightHUD.attributes("-alpha", 1)                                                # Making the HUD windown transparent 

#righttext = Text(rightHUD, height=2, width=30, font = ('Comic Sans', 30, 'bold'))
#righttext.pack()
#righttext.insert(END, hudText)

# Set bottom bar attributes
bottom = Tk()
bottom.tk_setPalette(background='#FFFFFF')
bottom.geometry('%dx%d+%d+%d' % (screenWidth, 56, 0, screenHeight - 56))
bottom.overrideredirect(1)                                                      # Removing borders
bottom.lift()
bottom.wm_attributes("-topmost", True)

# Run mode
def run():
        global mainproc, subproc1, subproc2
        # Setting button states.
        stereobutton['state']=DISABLED
        trackingbutton['state']=DISABLED
        endbutton['state']=NORMAL

        mainproc = subprocess.Popen('python main_client.py '+ip.get())
        subproc1 = subprocess.Popen('python server_camerastreamD5000.py')
        subproc2 = subprocess.Popen('python server_camerastream5001.py') 
        
        #time.sleep(10)                                                          # HUD alive time
        #leftHUD.destroy()
        #rightHUD.destroy()
        
# Tracking mode
def tracking():
        global mainproc, subproc1
        stereobutton['state']=DISABLED
        trackingbutton['state']=DISABLED
        mainproc = subprocess.Popen('python main_client_tracking.py '+ip.get())
        subproc1 = subprocess.Popen('python server_camerastream5000.py')
        time.sleep(10)
        end()

# End current video stream
def end():
        stereobutton['state']=NORMAL
        trackingbutton['state']=NORMAL
        endbutton['state']=DISABLED
        try:
                subproc2.kill()
        except:
                None
        finally:
                subproc1.kill()
                mainproc.kill()
                                
# End video and also close GUI           
def endgui():
        try:
                mainproc.kill()
                subproc1.kill()
                subproc2.kill()
        except:
                None
        finally:
                root.destroy()
                background.destroy()
                bottom.destroy()

                #HUD windows
                #leftHUD.destroy()
                #rightHUD.destroy()

# Place buttons
stereobutton = Button(root, highlightthickness=0, text="Run", fg="black", command = run)
stereobutton.place(x=100, y=18)

trackingbutton = Button(root, highlightthickness=0, text="Track", fg="black", command = tracking)
trackingbutton.place(x=200, y=18)

endbutton = Button(root, highlightthickness=0, text="End", state=DISABLED, fg="black", command = end)
endbutton.place(x=300, y=18)

quitbutton = Button(root, highlightthickness=0, text="Quit GUI", fg="black", command = endgui)
quitbutton.place(x=400, y=18)

# Place IP entry field
iplabel = Label(root, text="IP to main RPI")
iplabel.place(x= 550,y=22)

ip = Entry(root)
ip.insert(10, ipmain)
ip.place(x=650,y=24)

# Start root
root.mainloop()