from lib.fontObjects import doodleContour, doodlePoint, doodleComponent, doodleGlyph, doodleFont, doodleAnchor, robofabWrapper

###############
# identifiers #
###############

needIdentifiers = [
    doodleGlyph.DoodleGlyph,
    doodleContour.DoodleContour,
    doodlePoint.DoodlePoint,
    doodleComponent.DoodleComponent,
    doodleAnchor.DoodleAnchor,

    robofabWrapper.RobofabWrapperAnchor,
    robofabWrapper.RobofabWrapperComponent,
    robofabWrapper.RobofabWrapperContour,
    robofabWrapper.RobofabWrapperGlyph,
    robofabWrapper.RobofabWrapperPoint,
]

def _getIdentifier(self):
    return self.identifier

def _generateIdentifier(self):
    import uuid
    self.identifier = uuid.uuid4().hex
    return self.identifier

for obj in needIdentifiers:
    obj.identifier = None
    obj.getIdentifier = _getIdentifier
    obj.generateIdentifier = _generateIdentifier


##############
# guidelines #
##############

needGuidelines = [
    doodleGlyph.DoodleGlyph,
    doodleFont.DoodleFont,
    robofabWrapper.RobofabWrapperGlyph,
    robofabWrapper.RobofabWrapperFont,
]

for obj in needGuidelines:
    obj.guidelines = obj.guides
    obj.appendGuideline = obj.addGuide
    obj.removeGuideline = obj.removeGuide


###################
# transformations #
###################

needTransformations = [
    robofabWrapper.RobofabWrapperGlyph,
    robofabWrapper.RobofabWrapperContour,
    robofabWrapper.RobofabWrapperComponent,
]

for obj in needTransformations:
    obj.moveBy = obj.move
    if obj == robofabWrapper.RobofabWrapperComponent:
        obj.scaleBy = obj.scaleTransformation
    else:
        obj.scaleBy = obj.scale
    obj.rotateBy = obj.rotate
    obj.skewBy = obj.skew
    obj.transformBy = obj.transform


##########
# glyph  #
##########

needBounds = [
    robofabWrapper.RobofabWrapperGlyph,
    robofabWrapper.RobofabWrapperContour,
    robofabWrapper.RobofabWrapperComponent,
]

for obj in needBounds:
    obj.bounds = obj.box

###########
# changed #
###########

robofabWrapper.RobofabWrapperGlyph.changed = robofabWrapper.RobofabWrapperGlyph.update

#############
# markColor #
#############

robofabWrapper.RobofabWrapperGlyph.markColor = robofabWrapper.RobofabWrapperGlyph.mark

############################
# representation factories #
############################

import defcon

def _registerRepresentationFactory(cls, name, factory, destructiveNotifications=None):
    def factoryWrapper(glyph, font, *args, **kwargs):
        return factory(glyph, *args, **kwargs)
    defcon.addRepresentationFactory(name, factoryWrapper)

defcon.registerRepresentationFactory = _registerRepresentationFactory

# adding some new usefull mojo callbacks
import mojo.UI

from lib.scripting.codeEditor import CodeEditor
mojo.UI.CodeEditor = CodeEditor

###############
# test in RF1 #
###############

if __name__ == '__main__':
    # this must work in RF1
    f = CurrentFont()
    g = CurrentGlyph()
    g.skewBy((20, 10), origin=(100, -400))
    g.scaleBy((1.5, 2.0), origin=(100, 100))
    g.rotateBy(30, origin=(100, 100))
    g.changed()
    f.changed()
