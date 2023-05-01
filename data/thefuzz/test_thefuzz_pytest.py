from thefuzz import process


def test_process_warning(caplog):
    """Check that a string reduced to 0 by processor logs a warning to stderr"""

    query = ':::::::'
    choices = [':::::::']

    _ = process.extractOne(query, choices)

    logstr = ("Applied processor reduces "
              "input query to empty string, "
              "all comparisons will have score 0. "
              "[Query: ':::::::']")

    assert 1 == len(caplog.records)
    log = caplog.records[0]

    assert log.levelname == "WARNING"
    assert log.name == "thefuzz.process"
    assert logstr == log.message
