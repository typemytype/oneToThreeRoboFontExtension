# all required import to reroute in old modules
from fontPens import guessSmoothPointPen
from fontPens import transformPointPen
from fontPens import angledMarginPen
from fontPens import penTools
from fontPens import thresholdPen
from fontPens import flattenPen
from fontPens import digestPointPen
from fontPens import marginPen
from fontPens import printPointPen
from fontPens import printPen
from ufoLib import pointPen

from fontTools.pens import boundsPen
from fontTools.pens import reverseContourPen
from fontTools.misc import arrayTools
from fontTools.misc import bezierTools

# lets start
import warnings
import sys
from types import ModuleType

import mojo

from mojo.UI import setDefault

# force warnings to be displayed
setDefault("warningsLevel", "once")
warnings.resetwarnings()
warnings.simplefilter("once")


# a simple wrapper around a func/class thingy
# just to post a deprecated warning
def warnWrapper(func, rootModule, oldModule, newModule):
    def wrapper(*args, **kwargs):
        message = "%s is deprecated use '%s' instead of '%s'" % (rootModule, newModule, oldModule)
        warnings.warn(message, DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper

# a map of already mocked modules
mockedModules = {}
# a dict of callback to mock
# not all callbacs in each module needed to be mocked
toMock = {
    "robofab": {
        "world.CurrentFont": mojo.roboFont.CurrentFont,
        "world.CurrentGlyph": mojo.roboFont.CurrentGlyph,
        "world.RFont": mojo.roboFont.RFont,
        "world.RGlyph": mojo.roboFont.RGlyph,
        "world.OpenFont": mojo.roboFont.OpenFont,
        "world.NewFont": mojo.roboFont.NewFont,
        "world.AllFonts": mojo.roboFont.AllFonts,

        "objects.objects.objectsRF.RFont": mojo.roboFont.RFont,
        "objects.objects.objectsRF.RGlyph": mojo.roboFont.RGlyph,
        "objects.objects.objectsRF.OpenFont": mojo.roboFont.OpenFont,
        "objects.objects.objectsRF.NewFont": mojo.roboFont.NewFont,
        "objects.objects.objectsRF.AllFonts": mojo.roboFont.AllFonts,

        "pens.adapterPens.PointToSegmentPen": pointPen.PointToSegmentPen,
        "pens.adapterPens.SegmentToPointPen": pointPen.SegmentToPointPen,
        "pens.adapterPens.TransformPointPen": transformPointPen.TransformPointPen,
        "pens.adapterPens.GuessSmoothPointPen":  guessSmoothPointPen.GuessSmoothPointPen,

        "pens.angledMarginPen.AngledMarginPen": angledMarginPen.AngledMarginPen,
        "pens.angledMarginPen.getAngledMargins": angledMarginPen.getAngledMargins,
        "pens.angledMarginPen.setAngledLeftMargin": angledMarginPen.setAngledLeftMargin,
        "pens.angledMarginPen.setAngledRightMargin": angledMarginPen.setAngledRightMargin,
        "pens.angledMarginPen.centerAngledMargins": angledMarginPen.centerAngledMargins,
        "pens.angledMarginPen.guessItalicOffset": angledMarginPen.guessItalicOffset,

        "pens.boundsPen.ControlBoundsPen" : boundsPen.ControlBoundsPen,
        "pens.boundsPen.BoundsPen": boundsPen.BoundsPen,

        "pens.digestPen.DigestPointPen": digestPointPen.DigestPointPen,
        "pens.digestPen.DigestPointStructurePen": digestPointPen.DigestPointStructurePen,

        "pens.marginPen.MarginPen": marginPen.MarginPen,

        "pens.pointPen.AbstractPointPen": pointPen.AbstractPointPen,
        "pens.pointPen.BasePointToSegmentPen": pointPen.BasePointToSegmentPen,
        "pens.pointPen.PrintingPointPen": printPointPen.PrintPointPen,
        "pens.pointPen.SegmentPrintingPointPen": printPointPen.PrintPointPen,
        "pens.pointPen.PrintingSegmentPen": printPen.PrintPen,
        "pens.pointPen.SegmentPrintingPointPen": printPen.PrintPen,

        "pens.printingPens.PrintingPointPen":  printPointPen.PrintPointPen,
        "pens.printingPens.PrintingSegmentPen": printPen.PrintPen,
        "pens.printingPens.SegmentPrintingPointPen": printPointPen.PrintPointPen,

        "pens.reverseContourPointPen.ReverseContourPointPen": reverseContourPen.ReverseContourPen,

        "pens.filterPen.distance": penTools.distance,
        "pens.filterPen.ThresholdPen": thresholdPen.ThresholdPen,
        "pens.filterPen.thresholdGlyph": thresholdPen.thresholdGlyph,
        "pens.filterPen._estimateCubicCurveLength": penTools.estimateCubicCurveLength,
        "pens.filterPen._mid": penTools.middlePoint,
        "pens.filterPen._getCubicPoint": penTools.getCubicPoint,
        "pens.filterPen.FlattenPen": flattenPen.FlattenPen,
        "pens.filterPen.flattenGlyph": flattenPen.flattenGlyph,

        "interface.all.dialogs.Message": mojo.UI.Message,
        "interface.all.dialogs.AskString": mojo.UI.AskString,
        "interface.all.dialogs.AskYesNoCancel": mojo.UI.AskYesNoCancel,
        "interface.all.dialogs.GetFile": mojo.UI.GetFile,
        "interface.all.dialogs.GetFolder": mojo.UI.GetFolder,
        "interface.all.dialogs.PutFile": mojo.UI.PutFile,
        "interface.all.dialogs.SelectFont": mojo.UI.SelectFont,
        "interface.all.dialogs.SelectGlyph": mojo.UI.SelectGlyph,
        "interface.all.dialogs.FindGlyph": mojo.UI.FindGlyph,

        "misc.arrayTools.calcBounds": arrayTools.calcBounds,
        "misc.arrayTools.updateBounds": arrayTools.updateBounds,
        "misc.arrayTools.pointInRect": arrayTools.pointInRect,
        "misc.arrayTools.pointsInRect": arrayTools.pointsInRect,
        "misc.arrayTools.vectorLength": arrayTools.vectorLength,
        "misc.arrayTools.asInt16": arrayTools.asInt16,
        "misc.arrayTools.normRect": arrayTools.normRect,
        "misc.arrayTools.scaleRect": arrayTools.scaleRect,
        "misc.arrayTools.offsetRect": arrayTools.offsetRect,
        "misc.arrayTools.insetRect": arrayTools.insetRect,
        "misc.arrayTools.sectRect": arrayTools.sectRect,
        "misc.arrayTools.unionRect": arrayTools.unionRect,
        "misc.arrayTools.rectCenter": arrayTools.rectCenter,
        "misc.arrayTools.intRect": arrayTools.intRect,

        "misc.bezierTools.calcQuadraticBounds": bezierTools.calcQuadraticBounds,
        "misc.bezierTools.calcCubicBounds": bezierTools.calcCubicBounds,
        "misc.bezierTools.splitLine": bezierTools.splitLine,
        "misc.bezierTools.splitQuadratic": bezierTools.splitQuadratic,
        "misc.bezierTools.splitCubic": bezierTools.splitCubic,
        "misc.bezierTools.splitQuadraticAtT": bezierTools.splitQuadraticAtT,
        "misc.bezierTools.splitCubicAtT": bezierTools.splitCubicAtT,
        "misc.bezierTools.solveQuadratic": bezierTools.solveQuadratic,
        "misc.bezierTools.solveCubic": bezierTools.solveCubic,
    }
}

# start looping over all mocked root modules
for item, mocks in toMock.items():
    # create the root module
    rootModule = module = ModuleType(item)
    for mock, callback in mocks.items():
        moduleName = item
        # split on . to get sub modules
        parts = mock.split(".")
        for part in parts[:-1]:
            # get the sub module name
            moduleName += ".%s" % part
            # if we did mock it before
            if part not in mockedModules:
                # create a new mocked module
                subModule = mockedModules[part] = ModuleType(part)
                # set the mocked module in the sys.modules
                sys.modules[moduleName] = subModule
            else:
                # or get the mocked module
                subModule = mockedModules[part]
            # set the new mocked module as attr to the previous mocked part
            setattr(module, part, subModule)
            module = subModule
        # add the callback to the last mocked module
        setattr(module, parts[-1], warnWrapper(callback, item, "%s.%s" % (item, mock), callback.__module__))
        # reset the root
        module = rootModule
    # set the root in the sys.modules
    sys.modules[rootModule.__name__] = rootModule

###############
# test in RF3 #
###############

if __name__ == '__main__':
    # this must work in RF3
    f = CurrentFont()
    g = CurrentGlyph()
    g.skew(30, offset=(100, 100))
    g.scale((1.5, 2.0), center=(100, 100))
    g.rotate(30, offset=(100, 100))
    print("done")