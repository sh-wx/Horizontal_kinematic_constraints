# -* - coding:UTF-8 -*-
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)
class Horizontal_kinematic_constraintsDB(AFXDataDialog):
    def __init__(self, form):
        AFXDataDialog.__init__(self, form, 'Kunbang boundary',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            

        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
            
        l = FXLabel(p=self, text='Author: wx@BJUT', opts=JUSTIFY_LEFT)
        l.setFont( getAFXFont(FONT_BOLD) )
        l = FXLabel(p=self, text='Use after meshing the part', opts=JUSTIFY_LEFT)
        l.setFont( getAFXFont(FONT_BOLD) )
        frame = FXHorizontalFrame(self, 0, 0,0,0,0, 0,0,0,0)

        # Model combo
        # Since all forms will be canceled if the  model changes,
        # we do not need to register a query on the model.
        #
        self.RootComboBox_1 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Model:', tgt=form.modelNameKw, sel=0)
        self.RootComboBox_1.setMaxVisible(10)

        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.RootComboBox_1.appendItem(name)
        if not form.modelNameKw.getValue() in names:
            form.modelNameKw.setValue( names[0] )
        msgCount = 9
        form.modelNameKw.setTarget(self)
        form.modelNameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        self.form = form

        self.ComboBox_2 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Instance name:', tgt=form.instancenameKw, sel=0)
        self.ComboBox_2.setMaxVisible(10)
        msgCount4 = 45
        msgHandler4 = str(self.__class__).split('.')[-1] + '.onComboBox_2instanceChanged'           
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount4, msgHandler4) ) 

        frame1 = FXHorizontalFrame(self, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        ComboBox_8 = AFXComboBox(p=frame1, ncols=0, nvis=1, text='link direction(Only 3D):', tgt=form.alongdKw, sel=0)
        ComboBox_8.setMaxVisible(10)
        ComboBox_8.appendItem(text='X')
        ComboBox_8.appendItem(text='YZ')
        ComboBox_8.appendItem(text='X and YZ')
        
        ComboBox_5 = AFXComboBox(p=frame1, ncols=0, nvis=1, text='Vertical direction(Only 3D):', tgt=form.verticaldirectionKw, sel=0)
        ComboBox_5.setMaxVisible(10)
        ComboBox_5.appendItem(text='Y')
        ComboBox_5.appendItem(text='Z')

        
        ComboBox_6 = AFXComboBox(p=self, ncols=0, nvis=1, text='MPC or RIGIDBODY(Only 3D):', tgt=form.MPCorRIGIDBODYKw, sel=0)
        ComboBox_6.setMaxVisible(10)
        ComboBox_6.appendItem(text='MPC')
        ComboBox_6.appendItem(text='RIGIDBODY')
        
        frame2 = FXHorizontalFrame(self, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        ComboBox_7 = AFXComboBox(p=frame2, ncols=0, nvis=1, text='Auto or fromset:', tgt=form.setoraKw, sel=0)
        ComboBox_7.setMaxVisible(10)
        ComboBox_7.appendItem(text='Auto')
        ComboBox_7.appendItem(text='fromset')
        
        
        self.AA1=AFXTextField(p=frame2, ncols=20, labelText='nodeSet:', tgt=form.set1Kw,  sel=0)
        
        frame3 = FXHorizontalFrame(self, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        ComboBox_8 = AFXComboBox(p=frame3, ncols=0, nvis=1, text='Suppress or Resume:', tgt=form.addordecKw, sel=0)
        ComboBox_8.setMaxVisible(10)
        ComboBox_8.appendItem(text='Suppress')
        ComboBox_8.appendItem(text='Resume')
        
        ComboBox_9 = AFXComboBox(p=frame3, ncols=0, nvis=1, text='Modify: X or YZ', tgt=form.mdirectionKw, sel=0)
        ComboBox_9.setMaxVisible(10)
        ComboBox_9.appendItem(text='X')
        ComboBox_9.appendItem(text='YZ')
    
        self.AA2=AFXTextField(p=frame3, ncols=20, labelText='Number:', tgt=form.numberKw,  sel=0)
        
        fileName = os.path.join(thisDir, '1.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)
        self.currentmodelName = getCurrentContext()['modelName']
        self.form.modelNameKw.setValue(self.currentmodelName)
        mdb.models[self.currentmodelName].parts.registerQuery(self.updateComboBox_2instance)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)


        mdb.models[self.currentmodelName].parts.unregisterQuery(self.updateComboBox_2instance)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def processUpdates(self):
        if  self.form.setoraKw.getValue() == 'Auto':
            self.AA1.disable()
            self.AA1.disable()
        else:
            self.AA1.enable()
            self.AA1.enable()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        # Change parts container registration if the model has changed
    def onComboBox_2instanceChanged(self, sender, sel, ptr):    #自定义下拉框函数

        self.updateComboBox_2instance()
        return 1
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_2instance(self):                    #更新下拉框内容

        modelName = self.form.modelNameKw.getValue()
        # Update the names in the Parts combo
        self.ComboBox_2.clearItems()
        names = mdb.models[modelName].rootAssembly.instances.keys()#指向mdb的所有
        names.sort()
        for name in names:
            self.ComboBox_2.appendItem(name)                 #逐项添加到下拉框中
        if names:
            if not self.form.instancenameKw.getValue() in names:
                self.form.instancenameKw.setValue( names[0] )
        else:
            self.form.instancenameKw.setValue('')
        
        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )
