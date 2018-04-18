from mojo.roboFont import version

if version < "3.0":
    print("RoboFont 1")
    # in RoboFont 1.<something>
    import RF1
if version >= "3.0":
    print("RoboFont 3+")
    import RF3
