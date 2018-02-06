# oneToThreeRoboFontExtension

A RoboFont extension to help during the transition from RoboFont 1.8 to RoboFont 3, helping developers to make their code compatible with both versions.

## Background

RoboFont 3 introduces two significant changes which affect the scripting API:

| RoboFont 1  | RoboFont 3    |
| ----------- | ------------- |
| RoboFab API | FontParts API |
| Python 2    | Python 3      |

- [RoboFab vs. FontParts APIs](http://typemytype.gitlab.io/robofont_com/documentation/building-tools/toolkit/robofab-fontparts/)
- [Python 2 vs. Python 3](http://python-future.org/compatible_idioms.html#essential-syntax-differences)

## How to use oneToThree

1. Clone or download the repository.
2. Double-click the `.roboFontExt` file to install the extension in both RoboFont 1 *and* RoboFont 3.

### In RoboFont 1

The extension makes API changes from RF3 available in RF1:

- unique identifiers
- `font.guidelines` and `glyph.guidelines` (in addition to `font.guides` and `glyph.guides`)
- representation factories
- new `mojo.UI` callbacks

### In RoboFont 3

The extension routes deprecated RoboFab modules to their corresponding APIs in RF3:

- font objects
- pens
- dialogs
- misc tools
