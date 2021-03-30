def rows_to_dicts(rows):
    if isinstance(rows, list):
        for row in rows:
            if '_sa_instance_state' in row.__dict__:
                del row.__dict__['_sa_instance_state']
        return [dict(row.__dict__) for row in rows]
    else:
        if '_sa_instance_state' in rows.__dict__:
            del rows.__dict__['_sa_instance_state']
        return dict(rows.__dict__)
