CREATE TRIGGER IF NOT EXISTS REVERSE_TICKET_SEAT1
AFTER DELETE ON RECORD
FOR EACH ROW
BEGIN
    UPDATE TRAIN SET SEAT1_NUM=SEAT1_NUM+1 WHERE TRAINID=OLD.TRAINID AND OLD.SEATLEVEL='一等座';
END;

CREATE TRIGGER IF NOT EXISTS REVERSE_TICKET_SEAT2
AFTER DELETE ON RECORD
FOR EACH ROW
BEGIN
    UPDATE TRAIN SET SEAT2_NUM=SEAT2_NUM+1 WHERE TRAINID=OLD.TRAINID AND OLD.SEATLEVEL='二等座';
END;

CREATE TRIGGER IF NOT EXISTS REVERSE_TICKET_SEAT3
AFTER DELETE ON RECORD
FOR EACH ROW
BEGIN
    UPDATE TRAIN SET SEAT3_NUM=SEAT3_NUM+1 WHERE TRAINID=OLD.TRAINID AND OLD.SEATLEVEL='无座';
END;

CREATE INDEX IDX_TRAIN_TRAINID ON TRAIN(TRAINID);

CREATE INDEX IDX_PASSENGER_ID  ON  PASSENGER(ID);

