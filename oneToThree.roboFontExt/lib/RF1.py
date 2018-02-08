import AppKit
from mojo.roboFont import version as roboFontVersion

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

def keyWordSwapper(func, **kwargsMap):
    def wrapper(self, *args, **kwargs):
        for search, replace in kwargsMap.items():
            if search in kwargs:
                kwargs[replace] = kwargs[search]
                del kwargs[search]
        func(self, *args, **kwargs)
    return wrapper


def skewWrapper(self, value, origin):
    import math
    from fontTools.misc import transform
    x, y = value
    x = math.radians(x)
    y = math.radians(y)
    if origin:
        ox, oy = origin
    else:
        ox = oy = 0
    t = transform.Identity.translate(-ox, -oy).skew(x=x, y=y).translate(ox, oy)
    self.transform(tuple(t))


for obj in needTransformations:
    obj.moveBy = obj.move
    if obj == robofabWrapper.RobofabWrapperComponent:
        obj.scaleBy = obj.scaleTransformation
    else:
        obj.scaleBy = keyWordSwapper(obj.scale, origin="center")
    obj.rotateBy = keyWordSwapper(obj.rotate, origin="offset")
    obj.skewBy = skewWrapper
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

def _set_changed(self, value):
    self.update()

def _get_changed(parent):
    class callback(object):

        def __init__(self):
            parent.update()

        def __bool__(self):
            return parent.naked().dirty

    return callback

robofabWrapper.RobofabWrapperGlyph.changed = property(_get_changed, _set_changed)
robofabWrapper.RobofabWrapperFont.changed = property(_get_changed, _set_changed)

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

# adding some new useful mojo callbacks
import mojo.UI

from lib.scripting.codeEditor import CodeEditor
mojo.UI.CodeEditor = CodeEditor

####################
# Change App Title #
####################

menu = AppKit.NSApp().mainMenu()
roboFontItem = menu.itemWithTitle_("RoboFont")
if roboFontItem:
    txt = "RoboFont %s" % roboFontVersion
    attrTxt = AppKit.NSAttributedString.alloc().initWithString_attributes_(txt, {AppKit.NSFontAttributeName: AppKit.NSFont.menuBarFontOfSize_(0)})
    roboFontItem.setAttributedTitle_(attrTxt)
    roboFontItem.submenu().setTitle_(txt)

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
    otfPath = f.path.replace('.ufo', '.otf')
    f.generate("otfcff")
    f.generate("otfcff", otfPath)
    print("done")