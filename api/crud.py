def save_events_to_db(events, db_session):
    for event in events:
        db_event = Event(name=event["name"], date=event["date"], info=event["info"])
        db_session.add(db_event)
    db_session.commit()
