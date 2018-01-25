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
    "robofab" : {
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