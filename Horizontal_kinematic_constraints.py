# -*- coding: utf-8 -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from numpy import *
import regionToolset
import numpy as np
import os
import time
import shutil
import math
def erweimessage(lnode,nodematrix,rongcha):
    xmin=min(nodematrix[:,1])
    xmax=max(nodematrix[:,1])
    ymax=max(nodematrix[:,2])
    ymin=min(nodematrix[:,2])
    zmax=max(nodematrix[:,3])
    zmin=min(nodematrix[:,3])
    left=[]
    ccleft=[]
    right=[]
    ccright=[]
    for i in range(lnode):
        if (abs(nodematrix[i, 1]-xmin)<rongcha)  :
            left=np.hstack((left,nodematrix[i, 0]))
            ccleft=np.hstack((ccleft,nodematrix[i, 2]))
        if (abs(nodematrix[i, 1]-xmax)<rongcha):
            right=np.hstack((right,nodematrix[i, 0]))
            ccright=np.hstack((ccright,nodematrix[i, 2]))
    cbleft=np.vstack((left,ccleft))
    cbright=np.vstack((right,ccright))
    cleft=cbleft.T[lexsort(-cbleft)].T
    cright=cbright.T[lexsort(-cbright)].T
    return cleft,cright
def sanweimessage(lnode,nodematrix,verticaldirection,rongcha):     
    left=[]
    lefty=[]
    leftz=[]
    right=[]
    righty=[]
    rightz=[]
    ahead=[]
    aheady=[]
    aheadz=[]
    behind=[]
    behindy=[]
    behindz=[]
    if verticaldirection=='Y':
        xmin=min(nodematrix[:,1])
        xmax=max(nodematrix[:,1])
        zmax=max(nodematrix[:,3])
        zmin=min(nodematrix[:,3]);
        for i in range(lnode):
            if abs(nodematrix[i, 1]-xmax)<rongcha :
                left=np.hstack((left,nodematrix[i, 0]))
                lefty=np.hstack((lefty,nodematrix[i, 2]))
                leftz=np.hstack((leftz,nodematrix[i, 3]))
            if abs(nodematrix[i, 1]-xmin)<rongcha :
                right=np.hstack((right,nodematrix[i, 0]))
                righty=np.hstack((righty,nodematrix[i, 2]))
                rightz=np.hstack((rightz,nodematrix[i, 3]))
            if abs(nodematrix[i, 3]-zmax)<rongcha :
                ahead=np.hstack((ahead,nodematrix[i, 0]))
                aheady=np.hstack((aheady,nodematrix[i, 1]))
                aheadz=np.hstack((aheadz,nodematrix[i, 2]))
            if abs(nodematrix[i, 3]-zmin)<rongcha :
                behind=np.hstack((behind,nodematrix[i, 0]))
                behindy=np.hstack((behindy,nodematrix[i, 1]))
                behindz=np.hstack((behindz,nodematrix[i, 2]))          
    else: 
        xmin=min(nodematrix[:,1])
        xmax=max(nodematrix[:,1])
        ymax=max(nodematrix[:,2])
        ymin=min(nodematrix[:,2])
        for i in range(lnode):       
            if abs(nodematrix[i, 1]-xmax)<rongcha :
                left=np.hstack((left,nodematrix[i, 0]))
                lefty=np.hstack((lefty,nodematrix[i, 2]))
                leftz=np.hstack((leftz,nodematrix[i, 3]))
            if abs(nodematrix[i, 1]-xmin)<rongcha :
                right=np.hstack((right,nodematrix[i, 0]))
                righty=np.hstack((righty,nodematrix[i, 2]))
                rightz=np.hstack((rightz,nodematrix[i, 3]))
            if abs(nodematrix[i, 2]-ymax)<rongcha :
                ahead=np.hstack((ahead,nodematrix[i, 0]))
                aheady=np.hstack((aheady,nodematrix[i, 1]))
                aheadz=np.hstack((aheadz,nodematrix[i, 3]))
            if abs(nodematrix[i, 2]-ymin)<rongcha :
                behind=np.hstack((behind,nodematrix[i, 0]))
                behindy=np.hstack((behindy,nodematrix[i, 1]))
                behindz=np.hstack((behindz,nodematrix[i, 3]))    
    clefta=  np.vstack((left,lefty,leftz))
    crighta= np.vstack((right,righty,rightz))
    caheada= np.vstack((ahead,aheady,aheadz))
    cbehinda=np.vstack((behind,behindy,behindz))
    return clefta,crighta,caheada,cbehinda
def getfromset(modelName,set1):
    nodeset=mdb.models[modelName].rootAssembly.sets[set1]
    nodematrix = np.zeros((len(nodeset.nodes), 4))
    for i in range(len(nodeset.nodes)):
        nodematrix[i, :] =np.hstack((nodeset.nodes[i].label,nodeset.nodes[i].coordinates))
    return nodematrix
def main(modelName,verticaldirection,instancename,MPCorRIGIDBODY,setora,set1,alongd,number,mdirection,addordec):
    a=mdb.models[modelName].rootAssembly.instances[instancename]
    rongcha=0.0001
    print("Author:wx@BJUT")
    print("GNU General Public License")
    print("The default coordinate tolerance is 0.0001.")
    if setora == 'Auto':
        lnode=len(a.nodes)
        nodematrix = np.zeros((lnode, 4))
        for i in range(lnode):
            nodematrix[i, :] =np.hstack((a.nodes[i].label,a.nodes[i].coordinates))
    else:
        nodematrix=getfromset(modelName,set1)
        lnode=len(mdb.models[modelName].rootAssembly.sets[set1].nodes)
    zmax=max(nodematrix[:,3])
    zmin=min(nodematrix[:,3])
    if zmax !=0 or zmin!=0:
        dimension = 3
    else:
        dimension = 2
    if dimension == 2:
        cleft,cright=erweimessage(lnode,nodematrix,rongcha)
        nnode=cleft.shape[1]
        for ii in range(nnode):
            nodeleft=cleft[0,ii]
            boundarynode=a.nodes.sequenceFromLabels((int(nodeleft),))
            region1 = regionToolset.Region(nodes=boundarynode)
            noderight=cright[0,ii]
            boundarynode=a.nodes.sequenceFromLabels((int(noderight),))
            region2 = regionToolset.Region(nodes=boundarynode)
            mdb.models[modelName].MultipointConstraint(name='ConstraintMPC-'+str(ii+1),controlPoint=region1, surface=region2, mpcType=PIN_MPC, userMode=DOF_MODE_MPC, userType=0, csys=None)
    else:     
        lefts,rights,aheads,behinds=sanweimessage(lnode,nodematrix,verticaldirection,rongcha)
        if alongd=='X':
            if lefts.shape[1]!=rights.shape[1] :
                print("error: The number of elements on both faces needs to be the same")
            else:
                nnode=lefts.shape[1]
                lefts=lefts.T
                rights=rights.T
                indices_l = np.lexsort((lefts[:, 1], lefts[:, 2]))
                indices_r = np.lexsort((rights[:, 1], rights[:, 2]))
                lefts = lefts[indices_l]
                rights = rights[indices_r]
                for ii in range(nnode):            
                    nodeleft=lefts[ii,0]
                    boundarynode=a.nodes.sequenceFromLabels((int(nodeleft),))
                    region1 = regionToolset.Region(nodes=boundarynode)
                    noderight=rights[ii,0]
                    boundarynode=a.nodes.sequenceFromLabels((int(noderight),))
                    region2 = regionToolset.Region(nodes=boundarynode)
                    if MPCorRIGIDBODY=='RIGIDBODY':
                        mdb.models[modelName].RigidBody(name='ConstraintX-'+str(ii+1), refPointRegion=region1, pinRegion=region2)
                    else:
                        mdb.models[modelName].MultipointConstraint(name='ConstraintX-'+str(ii+1),controlPoint=region1, surface=region2, mpcType=PIN_MPC, userMode=DOF_MODE_MPC, userType=0, csys=None)  
        elif alongd=='YZ':
            if aheads.shape[1]!=behinds.shape[1] :
                print("error: The number of elements on both faces needs to be the same")
            else:
                nnode=aheads.shape[1]
                aheads=aheads.T
                behinds=behinds.T
                indices_l = np.lexsort((aheads[:, 1], aheads[:, 2]))
                indices_r = np.lexsort((behinds[:, 1], behinds[:, 2]))
                aheads = aheads[indices_l]
                behinds = behinds[indices_r]
                for ii in range(nnode):            
                    nodeleft=aheads[ii,0]
                    boundarynode=a.nodes.sequenceFromLabels((int(nodeleft),))
                    region1 = regionToolset.Region(nodes=boundarynode)
                    noderight=behinds[ii,0]
                    boundarynode=a.nodes.sequenceFromLabels((int(noderight),))
                    region2 = regionToolset.Region(nodes=boundarynode)
                    if MPCorRIGIDBODY=='RIGIDBODY':
                        mdb.models[modelName].RigidBody(name='ConstraintY-'+str(ii+1), refPointRegion=region1, pinRegion=region2)
                    else:
                        mdb.models[modelName].MultipointConstraint(name='ConstraintY-'+str(ii+1),controlPoint=region1, surface=region2, mpcType=PIN_MPC, userMode=DOF_MODE_MPC, userType=0, csys=None) 
        else:
            if aheads.shape[1]!=behinds.shape[1] or lefts.shape[1]!=rights.shape[1] :
                print("Error: The number of elements on both faces needs to be the same")
            else:
                nnode=lefts.shape[1]
                lefts=lefts.T
                rights=rights.T
                indices_l = np.lexsort((lefts[:, 1], lefts[:, 2]))
                indices_r = np.lexsort((rights[:, 1], rights[:, 2]))
                lefts = lefts[indices_l]
                rights = rights[indices_r]
                for ii in range(nnode):            
                    nodeleft=lefts[ii,0]
                    boundarynode=a.nodes.sequenceFromLabels((int(nodeleft),))
                    region1 = regionToolset.Region(nodes=boundarynode)
                    noderight=rights[ii,0]
                    boundarynode=a.nodes.sequenceFromLabels((int(noderight),))
                    region2 = regionToolset.Region(nodes=boundarynode)
                    if MPCorRIGIDBODY=='RIGIDBODY':
                        mdb.models[modelName].RigidBody(name='ConstraintX-'+str(ii+1), refPointRegion=region1, pinRegion=region2)
                    else:
                        mdb.models[modelName].MultipointConstraint(name='ConstraintX-'+str(ii+1),controlPoint=region1, surface=region2, mpcType=PIN_MPC, userMode=DOF_MODE_MPC, userType=0, csys=None)  
                xnumber=ii+1
                nnode=aheads.shape[1]
                aheads=aheads.T
                behinds=behinds.T
                indices_l = np.lexsort((aheads[:, 1], aheads[:, 2]))
                indices_r = np.lexsort((behinds[:, 1], behinds[:, 2]))
                aheads = aheads[indices_l]
                behinds = behinds[indices_r]
                for ii in range(nnode):            
                    nodeleft=aheads[ii,0]
                    boundarynode=a.nodes.sequenceFromLabels((int(nodeleft),))
                    region1 = regionToolset.Region(nodes=boundarynode)
                    noderight=behinds[ii,0]
                    boundarynode=a.nodes.sequenceFromLabels((int(noderight),))
                    region2 = regionToolset.Region(nodes=boundarynode)
                    if MPCorRIGIDBODY=='RIGIDBODY':
                        mdb.models[modelName].RigidBody(name='ConstraintY-'+str(ii+1), refPointRegion=region1, pinRegion=region2)
                    else:
                        mdb.models[modelName].MultipointConstraint(name='ConstraintY-'+str(ii+1),controlPoint=region1, surface=region2, mpcType=PIN_MPC, userMode=DOF_MODE_MPC, userType=0, csys=None) 
                ynumber=ii+1
    if number != '' and number != '0' :
        if mdirection == 'X':
            num_constraints = int(xnumber / int(number))
            constraint_prefix = 'ConstraintX-'
        else:
            num_constraints = int(ynumber / int(number))
            constraint_prefix = 'ConstraintY-'
        for i in range(1,num_constraints+1):
            name1 = constraint_prefix + str(i * int(number))
            if i < num_constraints:  
                name2 = constraint_prefix + str(i * int(number) + 1)
                if addordec == 'Suppress':
                    mdb.models[modelName].constraints[name1].suppress()
                    mdb.models[modelName].constraints[name2].suppress()
                else:
                    mdb.models[modelName].constraints[name1].resume()
                    mdb.models[modelName].constraints[name2].resume()
            else:  
                if addordec == 'Suppress':
                    mdb.models[modelName].constraints[name1].suppress()
                else:
                    mdb.models[modelName].constraints[name1].resume()
    print("All Done! Enjoy!")           