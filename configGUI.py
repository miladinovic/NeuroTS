#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import datetime
import os
import shutil
import subprocess
import time
import tkFileDialog
import tkFileDialog as filedialog
import tkMessageBox
from shutil import ignore_patterns

import Local as l
import configIO as io
import run_csp_training
from belfrywidgets.wizard import *


def pt(string):
    print string

class configGUI:
    def __init__(self):
        #self.cfg=io.configReader()

        self.root = Tk()
        self.root.title("Initial Configuration Wizard")


        self.langID=1
        self.serverPath="C:\Program Files\openvibe-2.0.1\openvibe-acquisition-server.cmd"
        self.designerPath="C:\Program Files\openvibe-2.0.1\openvibe-designer.cmd"
        self.acquisitionScenarioPath= "Y:\Downloads\OpenVibeConfigurationTest\motor-imagery\motor-imagery-bci-1-acquisition.xml"
        self.trainingScenarioPath= "Y:\Downloads\OpenVibeConfigurationTest\motor-imagery\motor-imagery-bci-2-classifier-trainer.xml"
        self.onlineScenarioPath= "Y:\Downloads\OpenVibeConfigurationTest\motor-imagery\motor-imagery-bci-3-online.xml"
        self.filterBankScenarioPath = ""
        self.filterTestScenarioPath = ""

        self.experimentName = StringVar()


        self.experimentDescription = StringVar()

        self.neurofeedbackProtocolType = StringVar()
        self.neurofeedbackProtocolType.set("RIGHT HAND")
        self.configFilename = "config_rightHand.ini"



        self.subjectID = IntVar()
        self.subjectID.set(1  )
        self.session = IntVar()
        self.session.set(1)


        self.autoPlayAcquisition= BooleanVar()
        self.autoPlayAcquisition.set(True)

        self.autoPlayTraining= BooleanVar()
        self.autoPlayTraining.set(True)

        self.cspFilterTraining = BooleanVar()
        self.cspFilterTraining.set(True)

        self.cspFilterTesting = BooleanVar()
        self.cspFilterTesting.set(True)

        self.ldaTraining = BooleanVar()
        self.ldaTraining.set(True)

        self.autoPlayOnline= BooleanVar()
        self.autoPlayOnline.set(True)

        self.experimentPath = StringVar()




        #init ini reader to read configuration file
        self.iniReader = io.configReader(self.configFilename)
        self.initConfig()

    def initConfig(self):
        self.experimentPath.set(self.iniReader.getLastExperimentPath())
        self.serverPath = self.iniReader.getServerPath()
        self.designerPath = self.iniReader.getDesignerPath()
        self.acquisitionScenarioPath = self.iniReader.getAcquisitionScenarionPath()
        self.trainingScenarioPath = self.iniReader.getTrainingScenarioPath()
        self.onlineScenarioPath = self.iniReader.getOnlineScenarioPath()
        self.filterBankScenarioPath = self.iniReader.getFilterBankScenario()
        self.filterTestScenarioPath = self.iniReader.getTestScenarioPath()

        # read the ini file of the experiment
        if len(self.iniReader.config.read(self.experimentPath.get() + "\experiment.ini")) <= 0:
            self.experimentPathExist = False

            self.experimentName.set("")
            self.experimentDescription.set("")
        else:
            self.experimentPathExist = True
            self.readExperimentVariables()







    def readExperimentVariables(self):


        if len(self.iniReader.config.read(self.experimentPath.get()+"\experiment.ini"))<=0:
            self.experimentName.set("")
            self.experimentDescription.set("")
            return

        try:
            self.experimentName.set(self.iniReader.configSectionMap("Experiment")["experiment name"])
        except:
            print "No name field"
            self.experimentName.set("")

        try:
            self.experimentDescription.set(self.iniReader.configSectionMap("Experiment")["experiment description"])
        except:
            self.experimentDescription.set("")
            print "No description field"




    def center(self,toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - (size[1]+0.1*size[1])/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def displayWizard(self):



        serverPath = StringVar()
        serverPath.set(self.serverPath)

        designerPath = StringVar()
        designerPath.set(self.designerPath)

        acquisitionPath = StringVar()
        acquisitionPath.set(self.acquisitionScenarioPath)

        trainingPath = StringVar()
        trainingPath.set(self.trainingScenarioPath)

        filterBankPath = StringVar()
        filterBankPath.set(self.filterBankScenarioPath)

        filterTestPath = StringVar()
        filterTestPath.set(self.filterTestScenarioPath)

        onlinePath = StringVar()
        onlinePath.set(self.onlineScenarioPath)













        wiz = Wizard(
            width=800,
            height=680,
            cancelcommand=lambda: exit(0),
            finishcommand=lambda: pt("Run"),
        )



        self.center(wiz)


        def disable_finish():
            #Change the name to "RUN"
            wiz.set_finish_text(l.gui.run(self.langID))
            wiz.set_cancel_text(l.gui.quit(self.langID))
            toggleNext(True)

            wiz.set_finish_enabled(False)


        def enable_finish():
            wiz.set_finish_enabled(True)

        def changeAqServerBatch():
            #value=filedialog.askdirectory(initialdir="/tmp/test")

            justPahtDir=os.path.dirname(os.path.abspath(self.serverPath))
            #value=tkFileDialog.askopenfilename(initialdir = justPahtDir,title = "Select file",filetypes = (("OpenVibe Scenario",("*.mxb","*.mxs","*.xml")),("all files","*.*")))
            path=tkFileDialog.askopenfilename(initialdir = justPahtDir,title = "Select file",filetypes = (("OpenVibe Batch",("*.bat","*.cmd")),("all files","*.*")))

            if not len(path)==0:
                serverPath.set(path)
                self.serverPath=path
            self.root.update()

        def changeDesignerBatch():

            justPahtDir=os.path.dirname(os.path.abspath(self.designerPath))
            path=tkFileDialog.askopenfilename(initialdir = justPahtDir,title = "Select file",filetypes = (("OpenVibe Batch",("*.bat","*.cmd")),("all files","*.*")))

            if not len(path)==0:
                designerPath.set(path)
                self.designerPath=path
            self.root.update()


        def selectAcquisitionScenario():

            justPahtDir=os.path.dirname(os.path.abspath(self.acquisitionScenarioPath))
            path=tkFileDialog.askopenfilename(initialdir = justPahtDir,title = "Select file",filetypes = (("OpenVibe Scenario",("*.mxb","*.mxs","*.xml")),("all files","*.*")))

            if not len(path)==0:
                acquisitionPath.set(path)
                self.acquisitionScenarioPath=path
            self.root.update()

        def selectTrainingScenario():

            justPahtDir=os.path.dirname(os.path.abspath(self.trainingScenarioPath))
            path=tkFileDialog.askopenfilename(initialdir = justPahtDir,title = "Select file",filetypes = (("OpenVibe Scenario",("*.mxb","*.mxs","*.xml")),("all files","*.*")))

            if not len(path)==0:
                trainingPath.set(path)
                self.trainingScenarioPath=path
            self.root.update()

        def selectOnlineScenario():

            justPahtDir=os.path.dirname(os.path.abspath(self.onlineScenarioPath))
            path=tkFileDialog.askopenfilename(initialdir = justPahtDir,title = "Select file",filetypes = (("OpenVibe Scenario",("*.mxb","*.mxs","*.xml")),("all files","*.*")))

            if not len(path)==0:
                onlinePath.set(path)
                self.onlineScenarioPath=path
            self.root.update()

        def selectFilterBankScenario():

            justPahtDir = os.path.dirname(os.path.abspath(self.filterBankScenarioPath))
            path = tkFileDialog.askopenfilename(initialdir=justPahtDir, title="Select file", filetypes=(
            ("OpenVibe Scenario", ("*.mxb", "*.mxs", "*.xml")), ("all files", "*.*")))

            if not len(path) == 0:
                filterBankPath.set(path)
                self.filterBankScenarioPath = path
            self.root.update()

        def selectTestFilterScenario():

            justPahtDir = os.path.dirname(os.path.abspath(self.filterTestScenarioPath))
            path = tkFileDialog.askopenfilename(initialdir=justPahtDir, title="Select file", filetypes=(
            ("OpenVibe Scenario", ("*.mxb", "*.mxs", "*.xml")), ("all files", "*.*")))

            if not len(path) == 0:
                filterTestPath.set(path)
                self.filterTestScenarioPath = path
            self.root.update()



        def editAcquisitionScenario():
            p = subprocess.Popen(self.designerPath +" --run-bg --no-session-management --open " + self.acquisitionScenarioPath, shell=False, stdout = subprocess.PIPE)
            pass

        def editTrainingScenario():
            p = subprocess.Popen(self.designerPath +" --run-bg --no-session-management --open " + self.trainingScenarioPath, shell=False, stdout = subprocess.PIPE)

            pass

        def editOnlineScenario():
            p = subprocess.Popen(self.designerPath +" --run-bg --no-session-management --open " + self.onlineScenarioPath, shell=False, stdout = subprocess.PIPE)


            pass

        def editFilterBankScenario():
            p = subprocess.Popen(
                self.designerPath + " --run-bg --no-session-management --open " + self.filterBankScenarioPath,
                shell=False, stdout=subprocess.PIPE)

            pass

        def editTestFilterScenario():
            p = subprocess.Popen(
                self.designerPath + " --run-bg --no-session-management --open " + self.filterTestScenarioPath,
                shell=False, stdout=subprocess.PIPE)

            pass


        #pane2

        def setExperimentLocation():

            justPahtDir=self.experimentPath.get()
            path=filedialog.askdirectory(initialdir = justPahtDir)

            if not len(path)==0:
                self.experimentPath.set(path)
                self.experimentPath.set(path)
                self.readExperimentVariables()
                print self.experimentName.get()

                #update


                #experimentNameVar.set(self.experimentName)
                #experimentDescriptionVar.set(self.experimentDescription)

            self.root.update()

        def setSubjectFolder():

            justPahtDir=self.experimentPath.get()
            path=filedialog.askdirectory(initialdir = justPahtDir)
            if not len(path)==0:
                self.subjectID.set(os.path.basename(os.path.normpath(path)))
                toggleNext(True)

            self.root.update()


            pass

        def pane0Next():

            # check selection
            if self.neurofeedbackProtocolType.get() == "RIGHT HAND":
                self.configFilename = "config_rightHand.ini"
                self.iniReader.setNewConfigFilename("config_rightHand.ini")
            if self.neurofeedbackProtocolType.get() == "LEFT HAND":
                self.iniReader.setNewConfigFilename("config_leftHand.ini")
                self.configFilename = "config_leftHand.ini"
            if self.neurofeedbackProtocolType.get() == "FEET":
                self.configFilename = "config_feet.ini"
                self.iniReader.setNewConfigFilename("config_feet.ini")


            # init player with new var
            self.iniReader = io.configReader(self.configFilename)
            self.initConfig()

            # init gui vars
            serverPath.set(self.serverPath)
            designerPath.set(self.designerPath)
            acquisitionPath.set(self.acquisitionScenarioPath)
            trainingPath.set(self.trainingScenarioPath)
            onlinePath.set(self.onlineScenarioPath)

            pass



        def pane1Next():

            #Save experiment dir
            writeConfig = io.configWriter(io.configReader(self.configFilename))
            writeConfig.configFilename = self.iniReader.configFilename
            writeConfig.serverPath=self.serverPath
            writeConfig.designerPath=self.designerPath
            writeConfig.acquisitionScenarioPath=self.acquisitionScenarioPath
            writeConfig.trainingScenarioPath=self.trainingScenarioPath
            writeConfig.onlineScenarioPath=self.onlineScenarioPath
            writeConfig.filterBankScenario = self.filterBankScenarioPath
            writeConfig.filterTestScenario = self.filterTestScenarioPath

            writeConfig.write()



        def pane2Next():

            #Save experiment dir
            writeConfig = io.configWriter(io.configReader(self.configFilename))
            writeConfig.configFilename = self.iniReader.configFilename
            writeConfig.serverPath = self.serverPath
            writeConfig.designerPath = self.designerPath
            writeConfig.acquisitionScenarioPath = self.acquisitionScenarioPath
            writeConfig.trainingScenarioPath = self.trainingScenarioPath
            writeConfig.onlineScenarioPath = self.onlineScenarioPath
            writeConfig.experimentPath=self.experimentPath.get()
            writeConfig.filterBankScenario = self.filterBankScenarioPath
            writeConfig.filterTestScenario = self.filterTestScenarioPath
            writeConfig.write()


            #Save experiment.ini for selected folder
            cfgfile = open(self.experimentPath.get()+"\experiment.ini",'w+')
            Config=ConfigParser.ConfigParser()

            section="Experiment"
            Config.add_section(section)
            Config.set(section,'experiment name',self.experimentName.get())
            Config.set(section,'experiment description',self.experimentDescription.get())
            Config.write(cfgfile)
            cfgfile.close()

            #create folders

            path =self.experimentPath.get()+"/"+str(self.subjectID.get())+"/"+str(self.session.get())
            if not os.path.exists(path):
                os.makedirs(path)
            if not os.path.exists(self.experimentPath.get() + "/SUBJECTS"):
                with open(self.experimentPath.get() + "/SUBJECTS", 'w+'): pass
            if not os.path.exists(self.experimentPath.get() + "/" + str(self.subjectID.get()) + "/SESSIONS"):
                with open(self.experimentPath.get() + "/" + str(self.subjectID.get()) + "/SESSIONS", 'w+'): pass
            else:
                tkMessageBox.showwarning("Warning!", "The data under this configuration already exist and it will be overwritten if you continue. To change Subject ID or Session please click 'Prev' button or continue if you know what are you doing!")
                backup_data(path)

        def backup_data(path):
            backup_dir = path + "/bak-" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')
            # os.makedirs(backup_dir)
            shutil.copytree(path, backup_dir, ignore=ignore_patterns('bak*'))
            pass



        def toggleNext(bool=True,savePathConfig=False):

            if savePathConfig:
                pane1Next()

            wiz.set_next_enabled(bool)
            pass


        #pane3

        def runAcqusitionServer():
            p = subprocess.Popen(self.serverPath,shell=False, stdout = subprocess.PIPE)
            pass

        def runAcquisition():

            argumentsVar = " --define Experiment_Path "+self.experimentPath.get()+" --define SubjectID "+str(self.subjectID.get())+" --define Session "+str(self.session.get())
            print argumentsVar

            if self.autoPlayAcquisition.get():
                p = subprocess.Popen(self.designerPath +" --run-bg --no-pause --no-gui --play " + self.acquisitionScenarioPath + argumentsVar, shell=False, stdout = subprocess.PIPE)
            else:
                p = subprocess.Popen(self.designerPath +" --run-bg --no-pause --no-session-management --open " + self.acquisitionScenarioPath + argumentsVar, shell=False, stdout = subprocess.PIPE)
            pass

        def runTraining():
            tkMessageBox.showinfo("Info",
                                  "Please be patient and don't click to any window on the window during training!")

            csp = run_csp_training.runCspTraining(self.designerPath, self.filterBankScenarioPath,
                                                  self.filterTestScenarioPath)

            if self.cspFilterTraining.get():
                csp.batchTraining(self.experimentPath.get(), str(self.subjectID.get()), str(self.session.get()))

            if self.cspFilterTesting.get():
                csp.runTesting(self.experimentPath.get(), str(self.subjectID.get()), str(self.session.get()))
                csp.seletFilters(self.experimentPath.get(), str(self.subjectID.get()), str(self.session.get()), 4)

            if self.ldaTraining.get():
                tkMessageBox.showinfo("Info",
                                      "The Classifier calibration will start now. At the end you can will see estimated accuracy of the system, after that you can close the window.")
                argumentsVar = " --define Experiment_Path " + self.experimentPath.get() + " --define SubjectID " + str(
                    self.subjectID.get()) + " --define Session " + str(self.session.get())
                p = subprocess.Popen(
                    self.designerPath + " --run-bg --no-gui  --no-pause --play-fast " + self.trainingScenarioPath + argumentsVar,
                    shell=False, stdout=subprocess.PIPE)
                (output, err) = p.communicate()
                p.wait()


            """
                        if self.autoPlayTraining.get():
                            file_ = open("ouput.txt", "w+")
                            p = subprocess.Popen(self.designerPath +" --no-gui --no-pause --play-fast " + self.trainingScenarioPath + argumentsVar, shell=False,stdout=subprocess.PIPE)
                            #stdout, stderr = p.communicate()
                            #print stdout
                        else:
                            p = subprocess.Popen(self.designerPath +" --run-bg --no-pause --no-session-management --open " + self.trainingScenarioPath + argumentsVar, shell=False, stdout = subprocess.PIPE)
                        pass"""


        def runOnline():
            argumentsVar = " --define Experiment_Path "+self.experimentPath.get()+" --define SubjectID "+str(self.subjectID.get())+" --define Session "+str(self.session.get())

            if self.autoPlayOnline.get():
                p = subprocess.Popen(self.designerPath +" --run-bg --no-pause --no-gui --play " + self.onlineScenarioPath + argumentsVar, shell=False, stdout = subprocess.PIPE)
            else:
                p = subprocess.Popen(self.designerPath +" --run-bg --no-pause --no-session-management --open " + self.onlineScenarioPath + argumentsVar, shell=False, stdout = subprocess.PIPE)
            pass

        def changeAcquistionAutoplay():
            pass

        def changeTrainingAutoplay():
            pass

        def changeOnlineAutoplay():
            pass

        def plotERP():
            # tkMessageBox.showinfo("Sorry!", "Sorry! :( Not yet implemented")
            import erp_plot as ploter
            plt = ploter.erp_plot()
            plt.plotERP(filename=self.experimentPath.get() + "/" + str(self.subjectID.get()) + "/" + str(
                self.session.get()) + "/training_data.gdf")

        def plotRawEEG():
            # tkMessageBox.showinfo("Sorry!", "Sorry! :( Not yet implemented")
            import erp_plot as ploter
            plt = ploter.erp_plot()
            plt.plotRawEEG(filename=self.experimentPath.get() + "/" + str(self.subjectID.get()) + "/" + str(
                self.session.get()) + "/training_data.gdf")

        def plotPSDLEFT():
            # tkMessageBox.showinfo("Sorry!", "Sorry! :( Not yet implemented")
            import erp_plot as ploter
            plt = ploter.erp_plot()
            plt.plotPSD(filename=self.experimentPath.get() + "/" + str(self.subjectID.get()) + "/" + str(
                self.session.get()) + "/training_data.gdf", cls="class1")

        def plotPSDRIGHT():
            # tkMessageBox.showinfo("Sorry!", "Sorry! :( Not yet implemented")
            import erp_plot as ploter
            plt = ploter.erp_plot()
            plt.plotPSD(filename=self.experimentPath.get() + "/" + str(self.subjectID.get()) + "/" + str(
                self.session.get()) + "/training_data.gdf", cls="class2")



        def runVideoFeedbackPlayer():

            info="SubjectID-->"+str(self.subjectID.get())+"..Session-->"+str(self.session.get())+"..Experiment name-->"+self.experimentName.get()+"..Path-->"+self.experimentPath.get()+"..Description-->"+self.experimentDescription.get()

            info=info.replace(" ","_")
            path= self.experimentPath.get()+"/"+str(self.subjectID.get())+"/"+str(self.session.get())


            #print info
            #print path
            #videoPlayer.runVideoPlayer()
            p = subprocess.Popen(
                "python videoPlayer.py " + path + " " + " " + self.iniReader.configFilename + " " + info, shell=False)






        wiz.set_default_button('next')

        ##########PANE 0 ############
        pane0 = wiz.add_pane('0', 'Init', entrycommand=disable_finish)
        lbl0 = Label(pane0, text="Welcome to the Video Feedback wizard\n\n", font='Helvetica 18 bold')

        lbl0.pack(side=TOP, fill=Y, expand=1)
        text = "Il Neurofeedback (NF) è un tipo di controllo a circuito chiuso che sfrutta la registrazione di un \n" \
               "segnale elettroencefalografico, per produrre un segnale sonoro e/o visivo da somministrare al \n" \
               "paziente. In questo modo il paziente impara ad influenzare l’attività cerebrale autoregolamentandola.\n" \
               "I segnali acustici e visivi sono dunque utilizzati come avvertimento per adottare strategie di controllo\n" \
               "ed imparare a modulare volontariamente i propri ritmi sensori-motori. A seconda della prevalenza\n" \
               "dell’handicap motorio, si deciderà se effettuare il trattamento di NF per migliorare la mobilità della\n" \
               "mano destra, sinistra o quella degli arti inferiori."
        lbl0 = Label(pane0, text=text)
        lbl0.pack(side=TOP, fill=Y, expand=1)

        midGroup = Frame(pane0)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        neuroFeedbackProtocol = Frame(midGroup)
        neuroFeedbackProtocol.pack(side=TOP, anchor="c", expand=1)
        labelSubjectID = Label(neuroFeedbackProtocol, text="Neurofeedback protocol type:", justify=LEFT)
        labelSubjectID.pack(side=LEFT, fill=Y, expand=0)
        OPTIONS = ["RIGHT HAND", "LEFT HAND", "FEET"]

        self.neurofeedbackProtocolType.set("RIGHT HAND")  # default value
        # w = apply(OptionMenu, (subjectID, self.subjectID) + tuple(OPTIONS))
        w = OptionMenu(neuroFeedbackProtocol, self.neurofeedbackProtocolType, *OPTIONS, command=toggleNext)
        w.pack(side=LEFT)

        # LOGOS
        photo = PhotoImage(file="logoB.pbm")
        photo2 = PhotoImage(file="logoA.pbm")

        logoBioing = Label(pane0, image=photo)
        logoBioing.pack(side=RIGHT, fill=BOTH, expand=1)

        logoBrainNew = Label(pane0, image=photo2)
        logoBrainNew.pack(side=RIGHT, fill=BOTH, expand=1)





        ##########PANE 1 ############
        pane1 = wiz.add_pane('one', 'First', entrycommand=pane0Next)

        lbl1 = Label(pane1, text="Welcome to the Video Feedback wizard\n\n",font='Helvetica 18 bold')
        """  "Please make sure that you have set EEG electrodes correctly and checked the impedances (Optimally bellow 5kOhms)"
                                 "WARNING! To make the wizard work properly, the initial openvibe.conf file has to be properly configured. If you are running "
                                 "this app for the first time please make sure that you edited the file located under C:\Program Files\openvibe-2xxx\share\openvibe\kernel\openvibe.conf "
                                 "by adding the line Include = ${Path_UserData}/openvibe.conf (or %appdata%/openvibe-2.0/openvibe.conf) at the end.", wraplength=500)"""
        lbl1.pack(side=TOP, fill=Y, expand=1)





        #Server

        midGroup=Frame(pane1)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        title = Label(midGroup,text="OpenVibe Acquisition Server Path",justify=CENTER,font='Helvetica 12 bold')
        title.pack(side=TOP, fill=BOTH, expand=0)

        lbl3 = Label(midGroup,textvariable=serverPath,justify=LEFT)
        lbl3.pack(side=LEFT, fill=BOTH, expand=0)


        b = Button(midGroup, text="Change", command=changeAqServerBatch)
        b.pack(side=LEFT, fill=BOTH, expand=0)

        #b2 = Button(midGroup, text="EDIT", command=changeAqServerBatch)
        #b2.pack(side=LEFT, fill=BOTH, expand=0)

        #Designer

        midGroup=Frame(pane1)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        title = Label(midGroup,text="OpenVibe Designer Path",justify=CENTER,font='Helvetica 12 bold')
        title.pack(side=TOP, fill=BOTH, expand=0)

        lbl3 = Label(midGroup,textvariable=designerPath,justify=LEFT)
        lbl3.pack(side=LEFT, fill=Y, expand=0)


        b = Button(midGroup, text="Change", command=changeDesignerBatch)
        b.pack(side=RIGHT, fill=Y, expand=0)

        #Aqusition

        midGroup=Frame(pane1)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        title = Label(midGroup,text="\nAcquisition Scenario",justify=CENTER,font='Helvetica 12 bold')
        title.pack(side=TOP, fill=BOTH, expand=0)

        lbl3 = Label(midGroup,textvariable=acquisitionPath,justify=LEFT)
        lbl3.pack(side=LEFT, fill=BOTH, expand=0)


        b = Button(midGroup, text="Change", command=selectAcquisitionScenario)
        b.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Edit", command=editAcquisitionScenario)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        # Trining CSP Bank Scenario

        midGroup=Frame(pane1)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        title = Label(midGroup, text="\nCSP Bank Scenario", justify=CENTER, font='Helvetica 12 bold')
        title.pack(side=TOP, fill=BOTH, expand=0)

        lbl3 = Label(midGroup, textvariable=filterBankPath, justify=LEFT)
        lbl3.pack(side=LEFT, fill=BOTH, expand=0)

        b = Button(midGroup, text="Change", command=selectFilterBankScenario)
        b.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Edit", command=editFilterBankScenario)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        # Trining

        midGroup = Frame(pane1)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        title = Label(midGroup, text="\nCSP Filter Testing Scenario", justify=CENTER, font='Helvetica 12 bold')
        title.pack(side=TOP, fill=BOTH, expand=0)

        lbl3 = Label(midGroup, textvariable=filterTestPath, justify=LEFT)
        lbl3.pack(side=LEFT, fill=BOTH, expand=0)

        b = Button(midGroup, text="Change", command=selectTestFilterScenario)
        b.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Edit", command=editTestFilterScenario)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        # Trining

        midGroup = Frame(pane1)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        title = Label(midGroup, text="\nClassifier Training Scenario", justify=CENTER, font='Helvetica 12 bold')
        title.pack(side=TOP, fill=BOTH, expand=0)

        lbl3 = Label(midGroup, textvariable=trainingPath, justify=LEFT)
        lbl3.pack(side=LEFT, fill=BOTH, expand=0)

        b = Button(midGroup, text="Change", command=selectTrainingScenario)
        b.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Edit", command=editTrainingScenario)
        b2.pack(side=LEFT, fill=BOTH, expand=0)
        #Online

        midGroup=Frame(pane1)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        title = Label(midGroup,text="\nOnline Scenario",justify=CENTER,font='Helvetica 12 bold')
        title.pack(side=TOP, fill=BOTH, expand=0)

        lbl3 = Label(midGroup,textvariable=onlinePath,justify=LEFT)
        lbl3.pack(side=LEFT, fill=BOTH, expand=0)


        b = Button(midGroup, text="Change", command=selectOnlineScenario)
        b.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Edit", command=editOnlineScenario)
        b2.pack(side=LEFT, fill=BOTH, expand=0)





        #LOGOS


        logoBioing = Label(pane1, image=photo)
        logoBioing.pack(side=RIGHT, fill=BOTH, expand=1)


        logoBrainNew = Label(pane1, image=photo2)
        logoBrainNew.pack(side=RIGHT, fill=BOTH, expand=1)

        ############# PANE 2 ############################################ PANE 2 ############################################ PANE 2 ############################################ PANE 2 ###############################

        pane2 = wiz.add_pane( 'two', 'Second',entrycommand=lambda:toggleNext(False,True))

        midGroup=Frame(pane2)
        midGroup.pack(side=TOP, anchor="c", expand=1)


        #Experiment location
        lbl1 = Label(midGroup, text="Please select the experiment folder (if not selected)",font='Helvetica 12 bold')
        lbl1.pack(side=TOP, fill=BOTH, expand=0)


        experimentLocation =Label(midGroup, textvariable=self.experimentPath)
        experimentLocation.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Edit", command=setExperimentLocation)
        b2.pack(side=LEFT, fill=BOTH, expand=0)


        midGroup=Frame(pane2)
        midGroup.pack(side=TOP, anchor="c", expand=1)


        #Experiment experiment information
        lbl1 = Label(midGroup, text="Experiment name")
        lbl1.pack(side=TOP, fill=BOTH, expand=0)


        experimentNameEnt =Entry(midGroup, width=20, textvariable=self.experimentName)
        experimentNameEnt.pack(side=LEFT, fill=BOTH, expand=0)


        #Desc

        midGroup=Frame(pane2)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        #Experiment experiment information
        lbl1 = Label(midGroup, text="Experiment Description")
        lbl1.pack(side=TOP, fill=BOTH, expand=0)


        experimentNameDesc =Entry(midGroup, width=100, textvariable=self.experimentDescription)
        experimentNameDesc.pack(side=LEFT, fill=BOTH, expand=0)


        #Subject matter
        lbl1 = Label(pane2, text="Subject Information",font='Helvetica 12 bold')
        lbl1.pack(side=TOP, anchor="c", expand=1)


        subjectID=Frame(pane2)
        subjectID.pack(side=TOP, anchor="c", expand=1)
        labelSubjectID = Label(subjectID, text="Subject ID:",justify=LEFT)
        labelSubjectID.pack(side=LEFT, fill=Y, expand=0)
        OPTIONS = range(1,100)

        self.subjectID.set(-1) # default value
        #w = apply(OptionMenu, (subjectID, self.subjectID) + tuple(OPTIONS))
        w= OptionMenu(subjectID,self.subjectID,*OPTIONS,command=toggleNext)
        w.pack(side=LEFT)

        """
        #Experiment location

        midGroup=Frame(pane2)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        lbl1 = Label(midGroup, text="Select subject folder: ")
        lbl1.pack(side=LEFT, fill=BOTH, expand=0)


        subjectFolder =Label(midGroup, textvariable=self.subjectID)
        subjectFolder.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Edit", command=setSubjectFolder)
        b2.pack(side=LEFT, fill=BOTH, expand=0)"""

        #sesssion id



        sessionID=Frame(pane2)
        sessionID.pack(side=TOP, anchor="c", expand=1)
        labelSubjectID = Label(sessionID, text="Session:",justify=LEFT)
        labelSubjectID.pack(side=LEFT, fill=Y, expand=0)
        OPTIONS2 = range(1,40)

        self.session.set(OPTIONS2[self.session.get()-1]) # default value
        w = apply(OptionMenu, (sessionID, self.session) + tuple(OPTIONS2))
        w.pack(side=LEFT)



        #LOGOS


        logoBioing = Label(pane2, image=photo)
        logoBioing.pack(side=RIGHT, fill=BOTH, expand=1)

        logoBrainNew = Label(pane2, image=photo2)
        logoBrainNew.pack(side=RIGHT, fill=BOTH, expand=1)


        ############# PANE 3 ############################################ PANE 3 ############################################ PANE 3 ############################################ PANE 2 ###############################

        pane3 = wiz.add_pane( 'three', 'Third',entrycommand=pane2Next)

        midGroup=Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)


        #Server
        lbl1 = Label(midGroup, text="Acquisition Server: ",font='Helvetica 12 bold')
        lbl1.pack(side=LEFT, fill=BOTH, expand=0)


        b2 = Button(midGroup, text="Run", command=runAcqusitionServer)
        b2.pack(side=LEFT, fill=BOTH, expand=0)


        #Acquisition

        midGroup=Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        lbl1 = Label(midGroup, text="Step 1. - Acquisition: ",font='Helvetica 12 bold',justify=LEFT)
        lbl1.pack(side=LEFT, fill=BOTH, expand=0)


        c = Checkbutton(midGroup, text="<---autoplay  ",variable=self.autoPlayAcquisition,command=changeAcquistionAutoplay)
        c.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Run", command=runAcquisition)
        b2.pack(side=LEFT, fill=BOTH, expand=0)


        #Training

        midGroup=Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        lbl1 = Label(midGroup, text="Step 2. - Training: ",font='Helvetica 12 bold',justify=LEFT)
        lbl1.pack(side=LEFT, fill=BOTH, expand=0)

        # c = Checkbutton(midGroup, text="<---autoplay  ",variable=self.autoPlayTraining,command=changeTrainingAutoplay)
        # c.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Run", command=runTraining)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        # Online

        midGroup = Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)
        lbl1 = Label(midGroup, text="Options", font='Helvetica 10 bold', justify=LEFT)
        lbl1.pack(side=LEFT, fill=BOTH, expand=0)

        midGroup = Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)
        c = Checkbutton(midGroup, text="CSP Filter Training  ", variable=self.cspFilterTraining,
                        command=changeTrainingAutoplay)
        c.pack(side=LEFT, fill=BOTH, expand=0)

        midGroup = Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)
        c = Checkbutton(midGroup, text="CSP Filter Evaluation  ", variable=self.cspFilterTesting,
                        command=changeTrainingAutoplay)
        c.pack(side=LEFT, fill=BOTH, expand=0)

        midGroup = Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)
        c = Checkbutton(midGroup, text="LDA Classifier Training  ", variable=self.ldaTraining,
                        command=changeTrainingAutoplay)
        c.pack(side=LEFT, fill=BOTH, expand=0)

        midGroup = Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)
        b2 = Button(midGroup, text="Plot Raw EEG", command=plotRawEEG)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Plot PSD (Class1 L)", command=plotPSDLEFT)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Plot PSD (Class2 R)", command=plotPSDRIGHT)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Plot ERP", command=plotERP)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        midGroup = Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        #Online

        midGroup=Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        lbl1 = Label(midGroup, text="Step 3. - Online: ",font='Helvetica 12 bold',justify=LEFT)
        lbl1.pack(side=LEFT, fill=BOTH, expand=0)


        c = Checkbutton(midGroup, text="<---autoplay  ",variable=self.autoPlayOnline,command=changeOnlineAutoplay)
        c.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Run", command=runOnline)
        b2.pack(side=LEFT, fill=BOTH, expand=0)

        #Online

        midGroup=Frame(pane3)
        midGroup.pack(side=TOP, anchor="c", expand=1)

        lbl1 = Label(midGroup, text="Step 4. - Video Feedback: ",font='Helvetica 12 bold',justify=LEFT)
        lbl1.pack(side=LEFT, fill=BOTH, expand=0)


       # c = Checkbutton(midGroup, text="<---autoplay  ",variable=self.autoPlayOnline,command=changeOnlineAutoplay)
       # c.pack(side=LEFT, fill=BOTH, expand=0)

        b2 = Button(midGroup, text="Run", command=runVideoFeedbackPlayer)
        b2.pack(side=LEFT, fill=BOTH, expand=0)


        #LOGOS


        logoBioing = Label(pane3, image=photo)
        logoBioing.pack(side=RIGHT, fill=BOTH, expand=1)

        logoBrainNew = Label(pane3, image=photo2)
        logoBrainNew.pack(side=RIGHT, fill=BOTH, expand=1)



        self.root.wm_withdraw()
        self.root.wait_window(wiz)









if __name__ == "__main__":
    def main():
        gui=configGUI()
        gui.displayWizard()

    main()
