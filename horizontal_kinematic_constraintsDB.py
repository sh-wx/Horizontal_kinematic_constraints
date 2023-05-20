from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class Horizontal_kinematic_constraintsDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

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
        self.RootComboBox_2 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Model:', tgt=form.ModelnameKw, sel=0)
        self.RootComboBox_2.setMaxVisible(10)

        names = mdb.models.keys()
        names.sort()
        for name in names:
            self.RootComboBox_2.appendItem(name)
        if not form.ModelnameKw.getValue() in names:
            form.ModelnameKw.setValue( names[0] )
        msgCount = 9
        form.ModelnameKw.setTarget(self)
        form.ModelnameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_2PartsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )

        # Parts combo
        #
        self.ComboBox_2 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Part:', tgt=form.PartNameKw, sel=0)
        self.ComboBox_2.setMaxVisible(10)

        self.form = form
        self.regModelName = None
        AFXTextField(p=self, ncols=12, labelText='Instance name:', tgt=form.instancenameKw, sel=0)
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

        # Register a query on parts
        #
        currentModelName = getCurrentContext()['modelName']
        self.form.ModelnameKw.setValue(currentModelName)
        mdb.models.registerQuery(self.updateComboBox_2Models, False)
        self.registerComboBox_2PartQuery(currentModelName)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        self.registerComboBox_2PartQuery(None)
        mdb.models.unregisterQuery(self.updateComboBox_2Models)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def registerComboBox_2PartQuery(self, modelName):

        if modelName == self.regModelName:
           return

        cbFunc = self.updateComboBox_2Parts
        modelKeys = mdb.models.keys()
        if self.regModelName in modelKeys:
           mdb.models[self.regModelName].unregisterQuery(cbFunc)
        self.regModelName = None

        if modelName in modelKeys:
           mdb.models[modelName].registerQuery(cbFunc, False)
           self.regModelName = modelName

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_2Models(self):

        # Update the names in the Models combo
        #
        self.RootComboBox_2.clearItems()
        names = mdb.models.keys()
        names.sort()
        for name in names:
           self.RootComboBox_2.appendItem(name)

        modelName = self.form.ModelnameKw.getValue()
        if not modelName in names:
           modelName = names[0]
        self.form.ModelnameKw.setValue(modelName) # Triggers parts combo update

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_2PartsChanged(self, sender, sel, ptr):

        self.updateComboBox_2Parts()
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_2Parts(self):

        # This is needed to handle lost registrations caused by model rename
        if not self.regModelName:
           return 1

        # Update the names in the Parts combo
        # 
        modelName = self.form.ModelnameKw.getValue()

        self.ComboBox_2.clearItems()
        names = mdb.models[modelName].parts.keys()
        names.sort()
        for name in names:
            self.ComboBox_2.appendItem(name)
        if names:
            if not self.form.PartNameKw.getValue() in names:
                self.form.PartNameKw.setValue( names[0] )
        else:
            self.form.PartNameKw.setValue('')

        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )

        # Change parts container registration if the model has changed
        self.registerComboBox_2PartQuery(modelName)

