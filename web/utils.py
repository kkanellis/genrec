import os

def scandir_filtered(dir, filters):
    with os.scandir(dir) as iterator:
        for entry in iterator:
            valid = True
            for filter, action in filters:
                if not filter(entry):
                    valid = False
                    if action:
                        action(entry)
                    break

            if valid:
                yield entry

