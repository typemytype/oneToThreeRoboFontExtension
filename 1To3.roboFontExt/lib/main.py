from mojo.roboFont import version

if version < "2.0.0":
    # in RoboFont 1.<something>
    import RF1
if version >= "2.0.0":
    import RF3