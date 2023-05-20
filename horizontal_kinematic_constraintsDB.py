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
            
        l = FXLabel(p=self, text='Author: sh-wx BJUT', opts=JUSTIFY_LEFT)
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
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_1PartsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )
        self.ComboBox_1 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Part:', tgt=form.PartNameKw, sel=0)
        self.ComboBox_1.setMaxVisible(10)
        self.form = form

        self.ComboBox_2 = AFXComboBox(p=self, ncols=0, nvis=1, text='Instance name:', tgt=form.instancenameKw, sel=0)
        self.ComboBox_2.setMaxVisible(10)
        msgCount4 = 45
        form.PartNameKw.setTarget(self)    #设置目标
        form.PartNameKw.setSelector(AFXDataDialog.ID_LAST+msgCount4)  #设置消息ID
        msgHandler4 = str(self.__class__).split('.')[-1] + '.onComboBox_2instanceChanged'           
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount4, msgHandler4) ) 

        ComboBox_5 = AFXComboBox(p=self, ncols=0, nvis=1, text='Vertical direction(Only 3D):', tgt=form.verticaldirectionKw, sel=0)
        ComboBox_5.setMaxVisible(10)
        ComboBox_5.appendItem(text='Y')
        ComboBox_5.appendItem(text='Z')
        fileName = os.path.join(thisDir, '1.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=self, text='', ic=icon)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)
        self.currentmodelName = getCurrentContext()['modelName']
        self.form.modelNameKw.setValue(self.currentmodelName)
        mdb.models[self.currentmodelName].parts.registerQuery(self.updateComboBox_1Parts)
        mdb.models[self.currentmodelName].parts.registerQuery(self.updateComboBox_2instance)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        mdb.models[self.currentmodelName].parts.unregisterQuery(self.updateComboBox_1Parts)
        mdb.models[self.currentmodelName].parts.unregisterQuery(self.updateComboBox_2instance)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_1PartsChanged(self, sender, sel, ptr):

        self.updateComboBox_1Parts()
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_1Parts(self):

        # This is needed to handle lost registrations caused by model rename


        # Update the names in the Parts combo
        # 
        modelName = self.form.modelNameKw.getValue()

        self.ComboBox_1.clearItems()
        names = mdb.models[modelName].parts.keys()
        names.sort()
        for name in names:
            self.ComboBox_1.appendItem(name)
        if names:
            if not self.form.PartNameKw.getValue() in names:
                self.form.PartNameKw.setValue( names[0] )
        else:
            self.form.PartNameKw.setValue('')

        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )

        # Change parts container registration if the model has changed
    def onComboBox_2instanceChanged(self, sender, sel, ptr):    #自定义下拉框函数

        self.updateComboBox_2instance()
        return 1
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_2instance(self):                    #更新下拉框内容

        modelName = self.form.modelNameKw.getValue()
        PartName = self.form.PartNameKw.getValue()
        # Update the names in the Parts combo

        if PartName!='':    #判断是否有part，避免在无零件时报错
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
