#Author- Ben Scire
#Description- Script to create arbitrary sketch points from csv and fit cross sections to them

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct
    file = app.activeDocument.name
    chop = file.split(' ')
    name = chop[0]


    if name.endswith("_R") or name.endswith("_BR"):
        orientation = 'right'
    else:
        orientation = 'left'

    # Get the root component of the active design.
    root = design.rootComponent
    sketches = root.sketches
    features = root.features



    def cs_mover(i, csPt, fitPt, a=1,b=0,c=0):
        #function that moves Cross section i to the fit pt as well as the IPs Bips and Splines
        #i = what were moving
        #csPt = from pt     fitPt = toPoint
        
        #add cross section curve and points to group and move together
        group = adsk.core.ObjectCollection.create()
        #Grab sketch based on i
        sk = root.sketches.itemByName('CS-'+ str(i))
        #add all sketch components to group
        for crv in sk.sketchCurves:
            group.add(crv)
        for pnt in sk.sketchPoints:
            group.add(pnt)
        #calculate vector from CS to fit point

        fromPt = extract_csPt(csPt)
        fitPt = extract_fitPt(fitPt)
        transform = adsk.core.Matrix3D.create()
        transform.translation = fromPt.vectorTo(fitPt)
    
        xv = transform.translation.x
        yv = transform.translation.y
        zv = transform.translation.z

        #specific translation modifiers for cross sections
        transform2 = adsk.core.Matrix3D.create()
        #need exceptions here

        if fitPt.x == 0 and fitPt.y == 0 and fitPt.z == 0:
            transform2.translation = adsk.core.Vector3D.create(0, 0, 0)
        else:
            if orientation == 'left':
                if csPt == 16 or csPt == 17:
                    transform2.translation = adsk.core.Vector3D.create(a*xv+0.25, b*yv, c*zv)
                elif csPt == 22 or csPt == 21:
                    transform2.translation = adsk.core.Vector3D.create(a*xv-0.25, b*yv, c*zv)
                else:
                    transform2.translation = adsk.core.Vector3D.create(a*xv, b*yv, c*zv)
            else:
                if csPt == 16 or csPt == 17:
                    transform2.translation = adsk.core.Vector3D.create(a*xv+0.25, b*yv, c*zv)
                elif csPt == 22 or csPt == 21:
                    transform2.translation = adsk.core.Vector3D.create(a*xv-0.25, b*yv, c*zv)
                else:
                    transform2.translation = adsk.core.Vector3D.create(a*xv, b*yv, c*zv)

                # if i == 23:
                #     transform2.translation = adsk.core.Vector3D.create(a*xv-0.2, b*yv, c*zv)
                # elif i == 15:
                #     transform2.translation = adsk.core.Vector3D.create(a*xv+0.3, b*yv, c*zv)

                #, fix cs-22 and cs-16, fix cs-23 and cs-15 for right legs  



        sk.move(group, transform2)

        #moves IP or BIP with the cross section


        #Specifics on moving spline points with CS, i changes for rail-3 and rail-4 due to unconnected spline points by the gears.

        spline_mover('rail-2',transform2,i-1)
        

        if orientation == 'right':
            if  0 < i < 5:
                spline_mover('Pipe-rail-1',transform2,i-1)
                ip_mover(i,transform2)
            elif i == 5:
                ip_mover(i-0.5,transform2)
                ip_mover(i,transform2)
                spline_mover('Pipe-rail-1',transform2,i-1)
                spline_mover('Pipe-rail-1',transform2,i)
                spline_mover('Pipe-rail-1',transform2,i+1)
            elif 5 < i < 14:
                spline_mover('Pipe-rail-1',transform2,i+1)
                ip_mover(i,transform2)
            elif i == 14 or i == 24:
                ip_mover(i,transform2,1)
        
            if i == 1:
                spline_mover('rail-3', transform2,i-1)
                spline_mover('rail-4', transform2,i-1)
                spline_mover('rail-3', transform2,i)
                spline_mover('rail-4', transform2,i)
            elif 1 < i < 4:
                spline_mover('rail-3', transform2,i)
                spline_mover('rail-4', transform2,i)            
            elif i == 4:
                spline_mover('rail-3', transform2,i)
                spline_mover('rail-4', transform2,i)
                spline_mover('rail-3', transform2,i+1)
                spline_mover('rail-4', transform2,i+1)
            elif i == 5:
                spline_mover('rail-3', transform2,i+1)
                spline_mover('rail-4', transform2,i+1)
                spline_mover('rail-3', transform2,i+2)
                spline_mover('rail-4', transform2,i+2)
                spline_mover('rail-3', transform2,i+3)
                spline_mover('rail-4', transform2,i+3)
                spline_mover('rail-1', transform2,i-1)
                spline_mover('rail-1', transform2,i)
                spline_mover('rail-1', transform2,i+1)
            elif 5 < i < 13:
                spline_mover('rail-3', transform2,i+3)
                spline_mover('rail-4', transform2,i+3)
            elif i == 13:
                spline_mover('rail-3', transform2,i+3)
                spline_mover('rail-4', transform2,i+3)
                spline_mover('rail-3', transform2,i+4)
                spline_mover('rail-4', transform2,i+4)
            elif i == 14:
                spline_mover('rail-3', transform2,i+4)
                spline_mover('rail-4', transform2,i+4)
                spline_mover('rail-3', transform2,i+5)
                spline_mover('rail-4', transform2,i+5)
            elif i == 15:
                spline_mover('rail-3', transform2,i+5)
                spline_mover('rail-4', transform2,i+5)
                spline_mover('rail-3', transform2,i+6)
                spline_mover('rail-4', transform2,i+6)
            elif 15 < i < 23:
                spline_mover('rail-3', transform2,i+6)
                spline_mover('rail-4', transform2,i+6)
            elif i == 23:
                spline_mover('rail-3', transform2,i+6)
                spline_mover('rail-4', transform2,i+6)
                spline_mover('rail-3', transform2,i+7)
                spline_mover('rail-4', transform2,i+7)
            elif i == 24:
                spline_mover('rail-3', transform2,i+7)
                spline_mover('rail-4', transform2,i+7)
                spline_mover('rail-3', transform2,i+8)
                spline_mover('rail-4', transform2,i+8)
            else:
                areWeGood = 'we good'

            if 1 <= i < 5:
                spline_mover('rail-1',transform2,i-1)
            elif i > 5:
                spline_mover('rail-1',transform2,i+1)
        else:
            if  0 < i < 9:
                spline_mover('Pipe-rail-1',transform2,i-1)
                ip_mover(i,transform2)
            elif i == 9:
                ip_mover(i+0.5,transform2)
                ip_mover(i,transform2)
                spline_mover('Pipe-rail-1',transform2,i-1)
                spline_mover('Pipe-rail-1',transform2,i)
                spline_mover('Pipe-rail-1',transform2,i+1)
            elif 9 < i < 14:
                spline_mover('Pipe-rail-1',transform2,i+1)
                ip_mover(i,transform2)
            elif i == 14 or i == 24:
                ip_mover(i,transform2,1)

            if i == 1:
                spline_mover('rail-3', transform2,i-1)
                spline_mover('rail-4', transform2,i-1)
                spline_mover('rail-3', transform2,i)
                spline_mover('rail-4', transform2,i)
            elif 1 < i < 9:
                spline_mover('rail-3', transform2,i)
                spline_mover('rail-4', transform2,i) 
            elif i == 9:
                spline_mover('rail-3', transform2,i)
                spline_mover('rail-4', transform2,i)
                spline_mover('rail-3', transform2,i+1)
                spline_mover('rail-4', transform2,i+1)
                spline_mover('rail-3', transform2,i+2)
                spline_mover('rail-4', transform2,i+2)
                spline_mover('rail-1', transform2,i-1)
                spline_mover('rail-1', transform2,i)
                spline_mover('rail-1', transform2,i+1)
            elif i == 10:
                spline_mover('rail-3', transform2,i+2)
                spline_mover('rail-4', transform2,i+2)
                spline_mover('rail-3', transform2,i+3)
                spline_mover('rail-4', transform2,i+3)
            elif 10 < i < 13:
                spline_mover('rail-3', transform2,i+3)
                spline_mover('rail-4', transform2,i+3)
            elif i == 13:
                spline_mover('rail-3', transform2,i+3)
                spline_mover('rail-4', transform2,i+3)
                spline_mover('rail-3', transform2,i+4)
                spline_mover('rail-4', transform2,i+4)
            elif i == 14:
                spline_mover('rail-3', transform2,i+4)
                spline_mover('rail-4', transform2,i+4)
                spline_mover('rail-3', transform2,i+5)
                spline_mover('rail-4', transform2,i+5)
            elif i == 15:
                spline_mover('rail-3', transform2,i+5)
                spline_mover('rail-4', transform2,i+5)
                spline_mover('rail-3', transform2,i+6)
                spline_mover('rail-4', transform2,i+6)
            elif 15 < i < 23:
                spline_mover('rail-3', transform2,i+6)
                spline_mover('rail-4', transform2,i+6)
            elif i == 23:
                spline_mover('rail-3', transform2,i+6)
                spline_mover('rail-4', transform2,i+6)
                spline_mover('rail-3', transform2,i+7)
                spline_mover('rail-4', transform2,i+7)
            elif i == 24:
                spline_mover('rail-3', transform2,i+7)
                spline_mover('rail-4', transform2,i+7)
                spline_mover('rail-3', transform2,i+8)
                spline_mover('rail-4', transform2,i+8)
            else:
                areWeGood = 'we good'


            if 1 <= i < 9:
                spline_mover('rail-1',transform2,i-1)
            elif i > 9:
                spline_mover('rail-1',transform2,i+1)


        #move gears with hinge cross section
        occ = root.occurrences.itemByName('HINGE:1')
        features2 = occ.component.features
        if i == 1:
            lHinge = adsk.core.ObjectCollection.create()
            lHinge.add(occ.component.bRepBodies.itemByName('OUTER_CAP'))
            lHinge.add(occ.component.bRepBodies.itemByName('TopGear2'))
            lHinge.add(occ.component.bRepBodies.itemByName('BotGear2'))

            moveFeats = features2.moveFeatures
            moveFeatureInput = moveFeats.createInput(lHinge, transform2)
            moveFeats.add(moveFeatureInput)

            cap = root.sketches.itemByName('cap_cut')
            allCap = adsk.core.ObjectCollection.create() 
            for crv in cap.sketchCurves:
                allCap.add(crv)
            for pnt in cap.sketchPoints:
                allCap.add(pnt)
            cap.move(allCap, transform2) 

        if i == 13:
            rHinge = adsk.core.ObjectCollection.create()
            rHinge.add(occ.component.bRepBodies.itemByName('INNER_CAP'))
            rHinge.add(occ.component.bRepBodies.itemByName('TopGear1'))
            rHinge.add(occ.component.bRepBodies.itemByName('BotGear1'))

            moveFeats = features2.moveFeatures
            moveFeatureInput = moveFeats.createInput(rHinge, transform2)
            moveFeats.add(moveFeatureInput)


    #function to move all IPs and BIPs with their CSs
    def ip_mover(i,transform, bip=0):
        if bip ==1:
            sk = root.sketches.itemByName('BIP-' + str(i))
        else:
            sk = root.sketches.itemByName('IP-' + str(i))

        group = adsk.core.ObjectCollection.create()
        #add all sketch components to group
        for crv in sk.sketchCurves:
            group.add(crv)
        for pnt in sk.sketchPoints:
            group.add(pnt)
        sk.move(group, transform) 

    def spline_mover(spline,transform,i):
        #function to move a specific spline point i, from the spline inputted
        sk = root.sketches.itemByName(spline)

        group = adsk.core.ObjectCollection.create()
        #add all sketch components to group
        spoint = sk.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(i)
        group.add(spoint)

        sk.move(group, transform)

    def loner_spline(orientation):
        #function to fix solo points below hinge
        transform = adsk.core.Matrix3D.create()
        transform2 = adsk.core.Matrix3D.create()
        s4 = root.sketches.itemByName('rail-4')
        s3 = root.sketches.itemByName('rail-3')
        l4 = adsk.core.ObjectCollection.create()
        r4 = adsk.core.ObjectCollection.create()
        l3 = adsk.core.ObjectCollection.create()
        r3 = adsk.core.ObjectCollection.create()
        r4pt = s4.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(18)
        l4pt = s4.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(26)
        r3pt = s3.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(18)
        l3pt = s3.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(26)
        l4.add(l4pt)
        r4.add(r4pt)
        l3.add(l3pt)
        r3.add(r3pt)

        if orientation == 'left':
            #medial
            avgX = ((s4.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(27).worldGeometry.x) + (s4.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(25).worldGeometry.x))/2
            l4X = l4pt.worldGeometry.x 
            transform.translation = adsk.core.Vector3D.create(avgX-l4X, 0, 0)

            #lateral
            baseX  = s4.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(17).worldGeometry.x
            dX = baseX - r4pt.worldGeometry.x
            transform2.translation = adsk.core.Vector3D.create(dX+0.2, 0, 0)

            s4.move(l4,transform)
            s4.move(r4,transform2)
            s3.move(l3,transform)
            s3.move(r3,transform2)
        else:
            avgX = ((s4.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(17).worldGeometry.x) + (s4.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(19).worldGeometry.x))/2
            r4X = r4pt.worldGeometry.x 
            transform.translation = adsk.core.Vector3D.create(avgX-r4X, 0, 0)

            #lateral
            baseX  = s4.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(27).worldGeometry.x
            dX = baseX - l4pt.worldGeometry.x
            transform2.translation = adsk.core.Vector3D.create(dX-0.2, 0, 0)

            s4.move(r4,transform)
            s4.move(l4,transform2)
            s3.move(r3,transform)
            s3.move(l3,transform2)




    def extract_csPt(i):
        #function to grab the same CS point from every CS
        sk = root.sketches.itemByName('CS-'+str(i))

        lineM = sk.sketchCurves.sketchLines.item(1)
        skpntM = lineM.startSketchPoint
        csPt = skpntM.worldGeometry

        return csPt

    def extract_fitPt(i):
        #function to grab coordinates of fitPt
        leg = root.meshBodies.item(0)
        legMesh = leg.mesh
        nodes = legMesh.nodeCoordinates

        sk = root.sketches.itemByName('CS-'+str(i))
        lineM = sk.sketchCurves.sketchLines.item(1)
        skpntM = lineM.startSketchPoint
        csPt = skpntM.worldGeometry

        nodeSlice = adsk.core.ObjectCollection.create()
        nodeSliceX = adsk.core.ObjectCollection.create()
        nodeSliceY = adsk.core.ObjectCollection.create()
        for node in nodes:
            if csPt.z-0.5 < node.z < csPt.z+0.5:
                nodeSlice.add(node)

        dX = 1000
        if 6<= i <= 8 or 18 <= i <= 20:
            for node in nodeSlice:
                if csPt.x - 0.5 < node.x < csPt.x + 0.5:
                    nodeSliceX.add(node)
            for node in nodeSliceX:
                if abs(node.y - csPt.y) < dX:
                    fitPt = node
                    dX = abs(node.y - csPt.y)
        elif i ==5 or i == 9 or i == 17 or i == 21:
            for node in nodeSlice:
                if csPt.y - 0.5 < node.y < csPt.y + 0.5:
                    nodeSliceY.add(node)
            for node in nodeSliceY:
                if abs(node.x - csPt.x) < dX:
                    fitPt = node
                    dX = abs(node.x - csPt.x)
        else:
            for node in nodeSlice:
                if abs(node.x - csPt.x) < dX:
                    fitPt = node
                    dX = abs(node.x - csPt.x)

        return fitPt

    # def global_move(i):
    #     cs_mover(i,4,4,0,1,0)
    #     #function to globally shift every sketch in the y-direction to allign with fit point depth (gears too)

    # for i in range(1,25):
    #     if i != 4:
    #         global_move(i)
    #     else:
    #         chill = 'chill'
    # global_move(4)  #have to do CS-4 last cuz thats my to and from point
    # cs_mover(1,1,1)
    # cs_mover(2,1,1)
    # cs_mover(3,3,3)
    for i in range(1,25):
        if i == 2 or i == 3 or i == 24 or i == 23:
            cs_mover(i,1,1)
        elif i == 11 or i == 12 or i == 14 or i == 15:
            cs_mover(i,13,13)
        elif 6 <= i <= 8 or 18 <= i <= 20:
            cs_mover(i,i,i,0,1)
        elif i != 1 and i != 13:
            cs_mover(i,i,i)
    cs_mover(1,1,1)
    cs_mover(13,13,13)

    #loner_spline(orientation)
