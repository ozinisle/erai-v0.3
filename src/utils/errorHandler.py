def handleError(exc_info, traceback, traceback_template):
    print("Error executing method >>> ")
    # exc_type, exc_obj, exc_tb = sys.exc_info()
    # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    # print("Unexpected error:", sys.exc_info())
    # print(exc_type, fname, exc_tb.tb_lineno)

    # http://docs.python.org/2/library/sys.html#sys.exc_info
    # most recent (if any) by default
    #exc_type, exc_value, exc_traceback = sys.exc_info()
    exc_type, exc_value, exc_traceback = exc_info

    '''
        Reason this _can_ be bad: If an (unhandled) exception happens AFTER this,
        or if we do not delete the labels on (not much) older versions of Py, the
        reference we created can linger.

        traceback.format_exc/print_exc do this very thing, BUT note this creates a
        temp scope within the function.
        '''

    traceback_details = {
        'filename': exc_traceback.tb_frame.f_code.co_filename,
        'lineno': exc_traceback.tb_lineno,
        'name': exc_traceback.tb_frame.f_code.co_name,
        'type': exc_type.__name__,
        'message': traceback.extract_tb(exc_traceback)
    }

    # So we don't leave our local labels/objects dangling
    del(exc_type, exc_value, exc_traceback)
    # This still isn't "completely safe", though!
    # "Best (recommended) practice: replace all exc_type, exc_value, exc_traceback
    # with sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]

    print
    print(traceback.format_exc())
    print
    print(traceback_template % traceback_details)
    print

    # traceback.print_exception()
