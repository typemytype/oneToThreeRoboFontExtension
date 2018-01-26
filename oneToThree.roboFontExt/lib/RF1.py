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


